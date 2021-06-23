import os
import re



GITIGNORE_FILE_PATH_REGEX=re.compile(r"[\\/]([!# ])")
GITIGNORE_SPECIAL_SET_CHARCTERS_REGEX=re.compile(r"([&~|])")
HTML_ATTRIBUTE_REGEX=re.compile(br'''([a-zA-Z0-9\-_]+)\s*(?:=\s*"((?:[^\"\\]|\\.)*))?"''')
HTML_TAG_JS_ATTRIBUTES=["onabort","onafterprint","onbeforeprint","onbeforeunload","onblur","oncanplay","oncanplaythrough","onchange","onclick","oncontextmenu","oncopy","oncuechange","oncut","ondblclick","ondrag","ondragend","ondragenter","ondragleave","ondragover","ondragstart","ondrop","ondurationchange","onemptied","onended","onerror","onfocus","onhashchange","oninput","oninvalid","onkeydown","onkeypress","onkeyup","onload","onloadeddata","onloadedmetadata","onloadstart","onmousedown","onmousemove","onmouseout","onmouseover","onmouseup","onmousewheel","onoffline","ononline","onpagehide","onpageshow","onpaste","onpause","onplay","onplaying","onpopstate","onprogress","onratechange","onreset","onresize","onscroll","onsearch","onseeked","onseeking","onselect","onstalled","onstorage","onsubmit","onsuspend","ontimeupdate","ontoggle","onunload","onvolumechange","onwaiting","onwheel"]
HTML_TAG_REGEX=re.compile(br"<([!/]?[a-zA-Z0-9\-_]+)\s*(.*?)\s*(/?)>",re.I|re.M|re.X)
JS_KEYWORDS=["break","case","catch","const","const","continue","debugger","default","delete","do","else","enum","false","finally","for","function","if","in","instanceof","let","new","null","of","return","switch","this","throw","true","try","typeof","var","var","void","while","with"]
JS_OPERATORS=["()=>","_=>","=>","...",">>>=",">>=","<<=","|=","^=","&=","+=","-=","*=","/=","%=",";",",","?",":","||","&&","|","^","&","===","==","=","!==","!=","<<","<=","<",">>>",">>",">=",">","++","--","+","-","*","/","%","!","~",".","[","]","{","}","(",")"]
JS_REGEX_LIST={"_end":re.compile(br"<\s*/script\s*?>"),"dict":re.compile(br"""{\s*(?:[$a-zA-Z0-9_]+|'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`)\s*:\s*"""),"dict_elem":re.compile(br""",\s*(?:[$a-zA-Z0-9_]+|'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|`(?:[^`\\]|\\.)*`)\s*:\s*"""),"float":re.compile(br"\d+\.\d*(?:[eE][-+]?\d+)?|^\d+(?:\.\d*)?[eE][-+]?\d+|^\.\d+(?:[eE][-+]?\d+)?"),"int":re.compile(br"0[xX][\da-fA-F]+|0[0-7]*|\d+"),"identifier":re.compile(br"\.?[$_a-zA-Z0-9]+(?:\.[$_a-zA-Z0-9]+)*"),"string":re.compile(br"""'(?:[^'\\]|\\.)*'|^"(?:[^"\\]|\\.)*"|^`(?:[^`\\]|\\.)*`"""),"regex":re.compile(br"\/(?![*+?])(?:[^\r\n\[/\\]|\\.|\[(?:[^\r\n\]\\]|\\.)*\])+\/(?!\/)[igm]{0,3}"),"line_break":re.compile(br"[\n\r]+|/\*(?:.|[\r\n])*?\*/"),"whitespace":re.compile(br"[\ \t]+|//.*?(?:[\r\n]|$)"),"operator":re.compile(bytes("|".join([re.sub(r"([\?\|\^\&\(\)\{\}\[\]\+\-\*\/\.])",r"\\\1",e) for e in JS_OPERATORS]),"utf-8"))}
JS_RESERVED_IDENTIFIERS=JS_KEYWORDS+["AggregateError","alert","arguments","Array","ArrayBuffer","AsyncFunction","AsyncGenerator","AsyncGeneratorFunction","atob","Atomics","BigInt","BigInt64Array","BigUint64Array","blur","Boolean","btoa","caches","cancelAnimationFrame","cancelIdleCallback","captureEvents","chrome","clearInterval","clearTimeout","clientInformation","close","closed","confirm","console","cookieStore","createImageBitmap","crossOriginIsolated","crypto","customElements","DataView","Date","decodeURI","decodeURIComponent","defaultStatus","defaultstatus","devicePixelRatio","document","encodeURI","encodeURIComponent","Error","escape","eval","EvalError","external","fetch","find","Float32Array","Float64Array","focus","frameElement","frames","Function","Generator","GeneratorFunction","getComputedStyle","getSelection","globalThis","history","Image","indexedDB","Infinity","innerHeight","innerWidth","Int16Array","Int32Array","Int8Array","InternalError","Intl","isFinite","isNaN","isSecureContext","JSON","length","localStorage","location","locationbar","Map","matchMedia","Math","menubar","moveBy","moveTo","NaN","navigator","Number","Object","open","openDatabase","opener","origin","originIsolated","outerHeight","outerWidth","pageXOffset","pageYOffset","parent","parseFloat","parseInt","performance","personalbar","postMessage","print","Promise","prompt","Proxy","queueMicrotask","RangeError","ReferenceError","Reflect","RegExp","releaseEvents","requestAnimationFrame","requestIdleCallback","resizeBy","resizeTo","screen","screenLeft","screenTop","screenX","screenY","scroll","scrollbars","scrollBy","scrollTo","scrollX","scrollY","self","sessionStorage","Set","setInterval","setTimeout","SharedArrayBuffer","showDirectoryPicker","showOpenFilePicker","showSaveFilePicker","speechSynthesis","status","statusbar","stop","String","styleMedia","Symbol","SyntaxError","toolbar","top","trustedTypes","TypeError","Uint16Array","Uint32Array","Uint8Array","Uint8ClampedArray","undefined","unescape","uneval","URIError","visualViewport","WeakMap","WeakSet","WebAssembly","webkitCancelAnimationFrame","webkitRequestAnimationFrame","webkitRequestFileSystem","webkitResolveLocalFileSystemURL","WebSocket","window"]
PYTHON_TOKEN_REGEX={"ignore":re.compile(br"\s*(?:\\\r?\n\s*)*(?:#[^\r\n]*)?"),"keyword":re.compile(br"(?:False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"),"identifier":re.compile(br"[a-zA-Z_][a-zA-Z_0-9]*(\s*\.\s*[a-zA-Z_][a-zA-Z_0-9]*)*"),"operator":re.compile(br"\~|\}|\|=|\||\{|\^=|\^|\]|\[|@=|@|>>=|>>|>=|>|==|=|<=|<<=|<<|<|;|:=|:|/=|//=|//|/|\.\.\.|\.|\->|\-=|\-|,|\+=|\+|\*=|\*\*=|\*\*|\*|\)|\(|\&=|\&|%=|%|!="),"integer":re.compile(br"(0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?[0-9])*))"),"float":re.compile(br"(([0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?|\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)"),"complex":re.compile(br"([0-9](?:_?[0-9])*[jJ]|(([0-9](?:_?[0-9])*\.(?:[0-9](?:_?[0-9])*)?|\.[0-9](?:_?[0-9])*)([eE][-+]?[0-9](?:_?[0-9])*)?|[0-9](?:_?[0-9])*[eE][-+]?[0-9](?:_?[0-9])*)[jJ])"),"string":re.compile(br"""(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)'''[^'\\]*(?:(?:\\.|'(?!''))[^'\\]*)*'''|(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)\"\"\"[^"\\]*(?:(?:\\.|"(?!""))[^"\\]*)*\"\"\"|((|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)'[^\n'\\]*(?:\\.[^\n'\\]*)*('|\\\r?\n)|(|rf|BR|rb|RF|Fr|RB|B|Rf|R|r|F|u|Br|Rb|fR|rB|f|U|rF|fr|b|FR|bR|br)"[^\n"\\]*(?:\\.[^\n"\\]*)*("|\\\r?\n))"""),"bracket":re.compile(br"\(|\[|\{|\)|\]|\}")}
TYPE_CLASS=3
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
			if (j<len(p) and p[j]=="]"):
				j+=1
			while (j<len(p) and p[j]!="]"):
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
		if ((ig is False or p[0] is True)):
			if (len(fnm)<len(p[1])):
				continue
			if (len(p[1][0].pattern)==2):
				ok=True
				for r,sfnm in zip(p[1],fnm):
					if (r.match(sfnm) is None):
						ok=False
						break
				if (ok is False):
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
				if (ok is False):
					continue
			if (p[0] is True):
				return False
			ig=True
	if (ig is True):
		return True
	return False



def _parse_python(fp,dt,o):
	tl=[]
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
			return
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
			t=(TYPE_CLASS if tl[i][1]==b"class" else TYPE_FUNCTION)
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
			sc.append((len(bf),{"t":t,"v":nm,"c":[],"l":[],"fl":[],"sln":sln,"soff":soff,"eln":0,"sz":0}))
			sc[-2][1]["c"].append(sc[-1][1])
		elif (tl[i][0]=="keyword" and tl[i][1] in [b"import",b"from"]):
			i+=1
			while (tl[i][0]=="ignore"):
				off+=len(tl[i][1])
				ln+=tl[i][1].count(b"\n")
				i+=1
			if (tl[i][0]!="operator" or tl[i][1]!=b"*"):
				if (tl[i][0]!="identifier"):
					raise RuntimeError
				sc[-1][1]["l"].append(fp[:-len(fp.split("/")[-1])]+str(tl[i][1],"utf-8")+".py")
		elif (tl[i][0]=="ignore"):
			v=tl[i][1].replace(b"\r\n",b"\n").split(b"\n")
			if (len(v)>1):
				bf=v[-1]
				while (len(sc)>0 and sc[-1][0]>len(bf)):
					sc[-1][1]["eln"]=ln
					sc[-1][1]["sz"]=off-sc[-1][1]["soff"]
					sc[-2][1]["sz"]+=sc[-1][1]["sz"]
					sc.pop()
			off+=len(tl[i][1])
			ln+=len(v)-1
		elif (tl[i][0]=="identifier"):
			sln=ln
			soff=off-len(tl[i][1])
			nm=tl[i][1]
			i+=1
			while (i<len(tl) and tl[i][0]=="ignore"):
				off+=len(tl[i][1])
				ln+=tl[i][1].count(b"\n")
				i+=1
			if (i<len(tl) and tl[i][0]=="operator" and tl[i][1]==b"("):
				sc[-1][1]["fl"].append((str(nm,"utf-8"),sln,soff))
		else:
			ln+=tl[i][1].count(b"\n")
		i+=1



def _parse_js(fp,dt,o):
	def _tokenize(s,c_rgx):
		i=0
		o=[]
		b=0
		while (i<len(s)):
			e=False
			for k,v in JS_REGEX_LIST.items():
				if (k=="regex" and c_rgx is False):
					continue
				mo=re.match(v,s[i:])
				if (mo!=None):
					m=mo.group(0)
					if (k=="_end"):
						return (o,i)
					elif (k=="line_break"):
						o+=[("operator",b";")]
					elif (k=="string" and m[:1]==b"`"):
						j=0
						ts=b""
						f=False
						while (j<len(m)):
							if (m[j:j+2]==b"${"):
								l,tj=_tokenize(m[j+2:],False)
								j+=tj+2
								o.append(("string"+("M" if f is True else "S"),(b"`"+ts[1:] if f is False else b"}"+ts)+b"${"))
								o.extend(l)
								ts=b""
								f=True
							else:
								ts+=m[j:j+1]
							j+=1
						o.append(("string"+("" if f is False else "E"),(b"}"+ts[:-1]+b"`" if f is True else ts)))
					elif (k!="whitespace"):
						if (k=="identifier" and str(m,"utf-8") in JS_KEYWORDS):
							k="keyword"
						elif (k=="identifier" and m.count(b".")>0 and m.split(b".")[0]==b"window" and str(m.split(b".")[1],"utf-8") in JS_RESERVED_IDENTIFIERS and str(m.split(b".")[1],"utf-8") not in JS_KEYWORDS):
							m=m[7:]
						if (k in ["operator","dict"]):
							if (m[:1]==b"{"):
								b+=1
							elif (m==b"}"):
								b-=1
								if (b==-1):
									return (o,i)
						o.append((k,m))
					i+=mo.end(0)
					e=True
					break
			if (e is True):
				continue
			raise RuntimeError(f"Unable to Match JS Regex: {str(s[i:],'utf-8')}")
		return (o,i)
	tl=_tokenize(dt,True)[0]



def _parse_html(fp,dt,o):
	i=0
	while (i<len(dt)):
		m=HTML_TAG_REGEX.search(dt[i:])
		if (m is None):
			break
		i+=m.end(0)
		t_nm=m.group(1)
		pm={}
		if (len(m.group(2))>0):
			for k,v in re.findall(HTML_ATTRIBUTE_REGEX,m.group(2)):
				if (str(k,"utf-8") in HTML_TAG_JS_ATTRIBUTES):
					raise RuntimeError("Unimplemented")
				pm[k]=v
		if (t_nm==b"script" and b"type" in pm and pm[b"type"]==b"text/javascript" and b"src" not in pm and b"async" not in pm and b"defer" not in pm):
			_parse_js(fp,dt[i:],o)



def _parse_dir(fp,gdt):
	fp=fp.replace("\\","/").rstrip("/")+"/"
	o={"t":TYPE_DIR,"v":fp.split("/")[-2],"c":[],"sz":0}
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
	try:
		for k in os.listdir(fp):
			if (os.path.isdir(fp+k) and (k!="docs" or len(gdt)<2)):
				if (_match_gitignore_path(gdt[-1],fp+k) is False):
					o["c"].append(_parse_dir(fp+k,gdt))
					o["sz"]+=o["c"][-1]["sz"]
			else:
				if (_match_gitignore_path(gdt[-1],fp+k) is False):
					e=k[len(k.split(".")[0]):]
					o["c"].append({"t":TYPE_FILE,"v":k,"c":[],"l":[],"fl":[],"sz":0})
					with open(fp+k,"rb") as f:
						dt=f.read()
						if (e==".py"):
							_parse_python(fp+k,dt,o["c"][-1])
						elif (e==".html"):
							_parse_html(fp+k,dt,o["c"][-1])
					o["c"][-1]["sz"]=os.stat(fp+k).st_size
					o["sz"]+=o["c"][-1]["sz"]
	except PermissionError:
		pass
	gdt.pop()
	return o



def _find_file(fp,dt):
	if (fp==dt["v"].lower()):
		return dt
	if (fp.startswith(dt["v"].lower())):
		fp=fp[len(dt["v"]):].lstrip("/")
		for k in dt["c"]:
			if (k["t"]!=TYPE_FUNCTION):
				f=_find_file(fp,k)
				if (f is not None):
					return f
	return None



def _generate_func_list(pfx,f_pfx,l,o):
	for k in l:
		v=(pfx+k["v"],(f_pfx+k["v"]).lower())
		if (v not in o):
			o.append(v)
		_generate_func_list(pfx+k["v"]+".",f_pfx+k["v"]+".",k["c"],o)



def _expand_calls(dt,r,f_dt,f_nm,b_fp):
	if (dt["t"]==TYPE_FILE or dt["t"]==TYPE_FUNCTION):
		ml=[]
		for k in dt["l"]:
			f=_find_file(k.lower()[len(b_fp):].strip("/"),r)
			if (f is None):
				continue
			_generate_func_list(k.split("/")[-1].split(".")[0]+".",k+":",f["c"],ml)
		_generate_func_list("",f_nm+":",f_dt["c"],ml)
		_generate_func_list("",f_nm+":",dt["c"],ml)
		nfl=[]
		for e,ln,off in dt["fl"]:
			for k in ml:
				if (e==k[0]):
					nfl.append((k[1],ln,off))
					break
		dt["fl"]=nfl
	for k in dt["c"]:
		if (k["t"]==TYPE_FUNCTION):
			_expand_calls(k,r,f_dt,f_nm,b_fp)
		else:
			_expand_calls(k,r,k,f_nm+"/"+k["v"],b_fp)



def visualize(fp,s_fp):
	dt=_parse_dir(fp,[[]])
	fp=fp.rstrip("/")
	_expand_calls(dt,dt,dt,fp.split("/")[-1],fp[:-len(fp.split("/")[-1])].rstrip("/"))
	with open(s_fp,"rb") as rf:
		return rf.read().replace(b"$$$DATA$$$",bytes(__import__("json").dumps(dt,separators=(",",":")),"utf-8"))



if (os.path.exists("build")):
	dl=[]
	for r,ndl,fl in os.walk("build"):
		r=r.replace("\\","/").strip("/")+"/"
		for d in ndl:
			dl.insert(0,r+d)
		for f in fl:
			os.remove(r+f)
	for k in dl:
		os.rmdir(k)
else:
	os.mkdir("build")
__file__=os.path.abspath(__file__).replace("\\","/")
with open("build/index.html","wb") as f:
	f.write(visualize(__file__[:-len(__file__.split("/")[-1])-4].rstrip("/")+"/","src/web/index.html"))
