from pathlib import Path
import re,json
BASE='https://jawad123-creator.github.io/Negocios.IA/'
NATIVE='<div class="ad-native" aria-label="Publicidad"><script async="async" data-cfasync="false" src="https://pl31172636.profitableratecpmnetwork.com/a609aa5baa281946f3978d91f6e7f4d5/invoke.js"></script><div id="container-a609aa5baa281946f3978d91f6e7f4d5"></div></div>'
BOX='<div class="ad-300" aria-label="Publicidad"><script>atOptions={"key":"f177569624c6dd37ca61725706854f70","format":"iframe","height":250,"width":300,"params":{}};</script><script src="https://www.highrevenueformat.com/f177569624c6dd37ca61725706854f70/invoke.js"></script></div>'
WIDE='<div class="ad-responsive ad-728" aria-label="Publicidad"><script>atOptions={"key":"4dc1319aa7ca2d9e4cee5cd26c710cf9","format":"iframe","height":90,"width":728,"params":{}};</script><script src="https://www.highrevenueformat.com/4dc1319aa7ca2d9e4cee5cd26c710cf9/invoke.js"></script></div><div class="ad-responsive ad-320" aria-label="Publicidad"><script>atOptions={"key":"3f17c555bf8527101418eba1f505d7d4","format":"iframe","height":50,"width":320,"params":{}};</script><script src="https://www.highrevenueformat.com/3f17c555bf8527101418eba1f505d7d4/invoke.js"></script></div>'
SMART='<div class="smartlink-box" aria-label="Recurso recomendado"><span>Recurso recomendado</span><a href="https://www.profitableratecpmnetwork.com/vtpmjm7xn?key=1a302b22acf124ab07d482bc7db8486a" target="_blank" rel="nofollow sponsored noopener">Ver recurso</a></div>'
POP='<script>(function(){try{if(!sessionStorage.getItem("nia_popunder_seen")){sessionStorage.setItem("nia_popunder_seen","1");var s=document.createElement("script");s.src="https://pl31198058.profitableratecpmnetwork.com/55/9f/e7/559fe752a937dcc608a0d073e947a5c3.js";s.async=true;document.body.appendChild(s)}}catch(e){}})();</script>'
SOCIAL='<script src="https://pl31198060.profitableratecpmnetwork.com/14/41/a6/1441a6308d99f419a586dc758e38f62a.js"></script>'
CSS='<style>.ad-native,.ad-300,.ad-responsive{margin:20px auto;display:flex;align-items:center;justify-content:center;overflow:hidden;min-height:0}.ad-native{width:100%;max-width:820px}.ad-300{width:300px;height:auto;min-height:0}.ad-responsive{width:100%;height:90px}.ad-320{display:none}.smartlink-box{margin:22px auto;padding:12px 16px;max-width:620px;display:flex;align-items:center;justify-content:space-between;gap:16px;border:1px solid rgba(128,128,128,.25);border-radius:10px;background:rgba(128,128,128,.06);font-size:.92rem}.smartlink-box a{font-weight:700;text-decoration:none}.smartlink-box span{opacity:.8}@media(max-width:600px){.ad-728{display:none}.ad-320{display:flex;height:50px}.smartlink-box{margin:18px auto;padding:11px 13px;font-size:.88rem}}</style>'
files=sorted(Path('articulos').glob('*.html'))
for p in files:
 s=p.read_text(encoding='utf-8')
 mt=re.search(r'<title>(.*?)</title>',s,re.S)
 if mt:
  t=re.sub(r'\s*\|\s*Negocios\.IA$','',mt.group(1)).strip()
  if len(t)>60:t=t[:57].rsplit(' ',1)[0]+'…'
  s=s[:mt.start(1)]+t+s[mt.end(1):]
 md=re.search(r'(<meta name="description" content=")([^"]*)(")',s)
 if md and len(md.group(2))>155:
  d=md.group(2)[:152].rsplit(' ',1)[0]+'…';s=s[:md.start(2)]+d+s[md.end(2):]
 # Clean old generated blocks, including malformed native wrappers from earlier runs.
 s=re.sub(r'<div[^>]*id="container-a609aa5baa281946f3978d91f6e7f4d5"[^>]*>\s*</div>','',s,flags=re.S|re.I)
 for pattern in [r'<div\s+class="ad-native"[^>]*>.*?</div>',r'<div\s+class="ad-300"[^>]*>.*?</div>',r'<div\s+class="ad-responsive[^>]*>.*?</div>',r'<div\s+class="smartlink-box"[^>]*>.*?</div>']:
  s=re.sub(pattern,'',s,flags=re.S|re.I)
 s=re.sub(r'<script[^>]+(?:profitableratecpmnetwork|highrevenueformat\.com)[^>]*>.*?</script>','',s,flags=re.S|re.I)
 s=re.sub(r'<script[^>]+(?:profitableratecpmnetwork|highrevenueformat\.com)[^>]*/>','',s,flags=re.S|re.I)
 s=re.sub(r'<script>\(function\(\)\{try\{if\(!sessionStorage\.getItem\("nia_popunder_seen"\).*?</script>','',s,flags=re.S)
 def schema(m):
  try:o=json.loads(m.group(1))
  except:return m.group(0)
  arr=o if isinstance(o,list) else [o]
  for x in arr:
   if isinstance(x,dict) and x.get('@type')=='Article':
    im=re.search(r'<img[^>]+src=["\']([^"\']+)',s)
    if im:x['image']=im.group(1)
    x['publisher']={'@type':'Organization','name':'Negocios.IA','url':BASE,'logo':{'@type':'ImageObject','url':BASE+'favicon.svg'}}
  return '<script type="application/ld+json">'+json.dumps(o if isinstance(o,list) else arr[0],ensure_ascii=False,separators=(',',':'))+'</script>'
 s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
 if '</head>' in s:s=s.replace('</head>',CSS+'</head>',1)
 hs=list(re.finditer(r'</h2>',s,re.I))
 if hs:
  n=len(hs)
  if n>=5:idxs=[max(0,n//5-1),max(0,n//2-1),max(0,4*n//5-1)]
  elif n>=3:idxs=[0,n//2,n-1]
  elif n==2:idxs=[0,1]
  else:idxs=[0]
  idxs=sorted(set(idxs)); placements=[(hs[idx].end(),ad) for idx,ad in zip(idxs,[BOX,NATIVE,WIDE])]
  if n>=4:placements.append((hs[n-2].end(),SMART))
  for pos,ad in sorted(placements,reverse=True):s=s[:pos]+ad+s[pos:]
 if SOCIAL not in s:s=s.replace('</body>',SOCIAL+'</body>',1)
 if 'nia_popunder_seen' not in s:s=s.replace('</body>',POP+'</body>',1)
 imgs=list(re.finditer(r'<img\b[^>]*>',s,re.I))
 for idx,m in reversed(list(enumerate(imgs))):
  tag=m.group(0)
  if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
  if idx>0 and 'loading=' not in tag:tag=tag[:-1]+' loading="lazy">'
  s=s[:m.start()]+tag+s[m.end():]
 s=s.replace('https://jawad123-creator.github.io/Negocios.IA/articulos/','/Negocios.IA/articulos/')
 p.write_text(s,encoding='utf-8')
