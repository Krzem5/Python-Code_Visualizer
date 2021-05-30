import os
import re
import os.path



GITIGNORE_FILE_PATH_REGEX=re.compile(r"[\\/]([!# ])")
GITIGNORE_SPECIAL_SET_CHARCTERS_REGEX=re.compile(r"([&~|])")
PYTHON_TOKEN_REGEX={"ignore":re.compile(br"\s*(?:\\\r?\n\s*)*(?:#[^\r\n]*)?"),"keyword":re.compile(br"(?:False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"),"identifier":re.compile(br"[a-zA-Z_][a-zA-Z_0-9]*(\s*\.\s*[a-zA-Z_][a-zA-Z_0-9]*)*"),"operator":re.compile(br"\~|\}|\|=|\||\{|\^=|\^|\]|\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\.\.\.|\.|\->|\-=|\-|,|\+=|\+|\*=|\*\*=|\*\*|\*|\)|\(|\&=|\&|%=|%|!="),"integer":re.compile(br"(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*))"),"float":re.compile(br"(([0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?|\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)"),"complex":re.compile(br"([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?|\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])"),"string":re.compile(br"""(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)'''[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''|(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)\"\"\"[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*\"\"\"|((|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)'[^\n'\\]*(?:\\.[^\n'\\]*)*('|\\\r?\n)|(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)"[^\n"\\]*(?:\\.[^\n"\\]*)*("|\\\r?\n))"""),"bracket":re.compile(br"\(|\[|\{|\)|\]|\}")}
TYPE_DIR=0
TYPE_FILE=1
TYPE_FUNCTION=2



def _create_gitignore_pattern(p):
	p=p.replace("\\","/").lower()
	ol=[]
	i=0
	while (i<len(p)):
		c=p[i]
		i+=1
		if (c=="*"):
			if (len(ol)==0 or ol[-1] is not None):
				ol.append(None)
		elif (c=="?"):
			ol.append(r".")
		elif (c=="["):
			j=i
			if (j<len(p) and p[j]=="!"):
				j+=1
			if j<len(p) and p[j]=="]":
				j+=1
			while j<len(p) and p[j]!="]":
				j+=1
			if (j>=len(p)):
				ol.append(r"\\[")
			else:
				l=p[i:j]
				if ("--" in l):
					cl=[]
					k=(i+2 if p[i]=="!" else i+1)
					while (True):
						k=p[k:j].find("-")
						if (k==-1):
							break
						cl.append(p[i:k])
						i+=1
						k+=3
					cl.append(p[i:j])
					l="-".join([e.replace("\\","\\\\").replace("-","\\-") for e in cl])
				else:
					l=l.replace("\\","\\\\")
				l=GITIGNORE_SPECIAL_SET_CHARCTERS_REGEX.sub(r"\\\1",l)
				i=j+1
				if (l[0]=='!'):
					ol.append(fr"[^{l[1:]}]")
				elif (l[0] in ("^","[")):
					ol.append(fr"[{chr(92)+l}]")
				else:
					ol.append(fr"[{l}]")
		else:
			ol.append(re.escape(c))
	o=""
	i=0
	while (i<len(ol) and ol[i] is not None):
		o+=ol[i]
		i+=1
	j=0
	while (i<len(ol)):
		i+=1
		if (i==len(ol)):
			o+=r".*"
			break
		l=""
		while (i<len(ol) and ol[i] is not None):
			l+=ol[i]
			i+=1
		if (i==len(ol)):
			o+=r".*"+l
		else:
			o+=fr"(?=(?P<_tmp_{j}>.*?{l}))(?P=_tmp_{j})"
			j+=1
	return re.compile(fr"{o}\Z",re.S)



def _match_gitignore_path(gdt,fp):
	fnm=fp.lower().replace("\\","/").lower().split("/")
	ig=False
	for p in gdt:
		if ((ig==False or p[0]==True)):
			if (len(fnm)<len(p[1])):
				continue
			if (len(p[1][0].pattern)==2):
				ok=True
				for r,sfnm in zip(p[1],fnm):
					if (r.match(sfnm) is None):
						ok=False
						break
				if (ok==False):
					continue
			else:
				ok=False
				for i in range(0,len(fnm)-len(p[1])+1):
					for r,sfnm in zip(p[1],fnm[i:]):
						if (r.match(sfnm) is None):
							break
					else:
						ok=True
						break
				if (ok==False):
					continue
			if (p[0]==True):
				return False
			ig=True
	if (ig==True):
		return True
	return False



def _parse_python(fp,o):
	tl=[]
	with open(fp,"rb") as f:
		dt=f.read()
		i=0
		while (i<len(dt)):
			ok=False
			for k,v in PYTHON_TOKEN_REGEX.items():
				m=v.match(dt[i:])
				if (m is not None and m.end(0)!=0):
					tl.append((k,m.group(0)))
					ok=True
					i+=m.end(0)
					break
			if (not ok):
				return []
	sc=[(0,o)]
	i=0
	off=0
	ln=1
	bf=b""
	while (i<len(tl)):
		off+=len(tl[i][1])
		if (tl[i][0]=="keyword" and tl[i][1] in [b"def",b"class"]):
			sln=ln
			soff=off-len(tl[i][1])
			i+=1
			while (tl[i][0]=="ignore"):
				off+=len(tl[i][1])
				ln+=tl[i][1].count(b"\n")
				i+=1
			if (tl[i][0]!="identifier"):
				raise RuntimeError
			nm=str(tl[i][1],"utf-8")
			while (tl[i][0]!="operator" or tl[i][1]!=b":"):
				if (tl[i][0]=="ignore"):
					off+=len(tl[i][1])
					ln+=tl[i][1].count(b"\n")
				i+=1
			i+=1
			if (tl[i][0]=="ignore"):
				v=tl[i][1].replace(b"\r\n",b"\n").split(b"\n")
				off+=len(tl[i][1])
				ln+=len(v)-1
				if (len(v)>1):
					bf=v[-1]
				i+=1
			sc.append((len(bf),{"t":TYPE_FUNCTION,"v":nm,"c":[],"l":[],"sln":sln,"soff":soff,"eln":0,"eoff":0}))
			sc[-2][1]["c"].append(sc[-1][1])
		elif (tl[i][0]=="keyword" and tl[i][1] in [b"import",b"from"]):
			sln=ln
			soff=off-len(tl[i][1])
			i+=1
			while (tl[i][0]=="ignore"):
				off+=len(tl[i][1])
				ln+=tl[i][1].count(b"\n")
				i+=1
			if (tl[i][0]!="operator" or tl[i][1]!=b"*"):
				if (tl[i][0]!="identifier"):
					raise RuntimeError
				sc[-1][1]["l"].append(str(tl[i][1],"utf-8"))
		elif (tl[i][0]=="ignore"):
			v=tl[i][1].replace(b"\r\n",b"\n").split(b"\n")
			if (len(v)>1):
				bf=v[-1]
				while (len(sc)>0 and sc[-1][0]>len(bf)):
					sc[-1][1]["eln"]=ln
					sc[-1][1]["eoff"]=off
					sc.pop()
			off+=len(tl[i][1])
			ln+=len(v)-1
		else:
			ln+=tl[i][1].count(b"\n")
		i+=1



def _parse_dir(fp,gdt):
	fp=fp.replace("\\","/").rstrip("/")+"/"
	o={"t":TYPE_DIR,"v":fp.split("/")[-2],"c":[]}
	gdt.append(gdt[-1])
	if (os.path.exists(fp+".gitignore")):
		with open(fp+".gitignore","r") as f:
			for ln in f.read().replace("\r\n","\n").split("\n"):
				if (ln.endswith("\n")):
					ln=ln[:-1]
				ln=ln.lstrip()
				if (not ln.startswith("#")):
					iv=False
					if (ln.startswith("!")):
						ln=ln[1:]
						iv=True
					while (ln.endswith(" ") and ln[-2:]!="\\ " and ln[-2:]!="/ "):
						ln=ln[:-1]
					ln=GITIGNORE_FILE_PATH_REGEX.sub(r"\1",ln)
					if (len(ln)>0):
						if ("**/" in ln):
							gdt[-1].append([iv,tuple(_create_gitignore_pattern(e) for e in ln.replace("**/","").split("/"))])
						gdt[-1].append([iv,tuple(_create_gitignore_pattern(e) for e in ln.split("/"))])
	for k in os.listdir(fp):
		if (os.path.isdir(fp+k)):
			if (_match_gitignore_path(gdt[-1],fp+k)==False):
				o["c"].append(_parse_dir(fp+k,gdt))
		else:
			if (_match_gitignore_path(gdt[-1],fp+k)==False):
				e=k[len(k.split(".")[0]):]
				if (e==".py"):
					o["c"].append({"t":TYPE_FILE,"v":k,"c":[],"l":[]})
					_parse_python(fp+k,o["c"][-1])
	gdt.pop()
	return o



def visualize(fp):
	return _parse_dir(fp,[[]])



__file__=os.path.abspath(__file__).replace("\\","/")
print(visualize(__file__[:-len(__file__.split("/")[-1])-4].rstrip("/")+"/"))
print(visualize("D:/K"))
