from pathlib import Path
import re,json
BASE='https://jawad123-creator.github.io/Negocios.IA/'
NATIVE='<div class="ad-native" aria-label="Publicidad"><script async="async" data-cfasync="false" src="https://pl31172636.profitableratecpmnetwork.com/a609aa5baa281946f3978d91f6e7f4d5/invoke.js"></script><div id="container-a609aa5baa281946f3978d91f6e7f4d5"></div></div>'
BOX='<div class="ad-300" aria-label="Publicidad"><script>atOptions={"key":"f177569624c6dd37ca61725706854f70","format":"iframe","height":250,"width":300,"params":{}};</script><script src="https://www.highrevenueformat.com/f177569624c6dd37ca61725706854f70/invoke.js"></script></div>'
WIDE='<div class="ad-responsive ad-728" aria-label="Publicidad"><script>atOptions={"key":"4dc1319aa7ca2d9e4cee5cd26c710cf9","format":"iframe","height":90,"width":728,"params":{}};</script><script src="https://www.highrevenueformat.com/4dc1319aa7ca2d9e4cee5cd26c710cf9/invoke.js"></script></div><div class="ad-responsive ad-320" aria-label="Publicidad"><script>atOptions={"key":"3f17c555bf8527101418eba1f505d7d4","format":"iframe","height":50,"width":320,"params":{}};</script><script src="https://www.highrevenueformat.com/3f17c555bf8527101418eba1f505d7d4/invoke.js"></script></div>'
SOCIAL='<script src="https://pl31198060.profitableratecpmnetwork.com/14/41/a6/1441a6308d99f419a586dc758e38f62a.js"></script>'
CSS='<style>.ad-native,.ad-300,.ad-responsive{margin:34px auto;display:flex;align-items:center;justify-content:center;overflow:hidden}.ad-native{width:100%;max-width:820px}.ad-300{width:300px;min-height:250px}.ad-responsive{width:100%;height:90px}.ad-320{display:none}@media(max-width:600px){.ad-728{display:none}.ad-320{display:flex;height:50px}}</style>'
files=sorted(Path('articulos').glob('*.html')); names=[p.name for p in files]
for i,p in enumerate(files):
 s=p.read_text(encoding='utf-8')
 mt=re.search(r'<title>(.*?)</title>',s,re.S)
 if mt:
  t=re.sub(r'\s*\|\s*Negocios\.IA$','',mt.group(1)).strip()
  if len(t)>60:t=t[:57].rsplit(' ',1)[0]+'…'
  s=s[:mt.start(1)]+t+s[mt.end(1):]
 md=re.search(r'(<meta name="description" content=")([^"]*)(")',s)
 if md and len(md.group(2))>155:
  d=md.group(2)[:152].rsplit(' ',1)[0]+'…';s=s[:md.start(2)]+d+s[md.end(2):]
 # Remove every previous ad placement, popup and Smartlink without touching normal content.
 s=re.sub(r'<div class="ad-native">.*?</div>|<div class="ad-300">.*?</div>|<div class="ad-responsive[^>]*>.*?</div>|<div class="smartlink-box">.*?</div>','',s,flags=re.S)
 s=re.sub(r'<script[^>]+(?:profitableratecpmnetwork|highrevenueformat\.com)[^>]+></script>','',s,flags=re.S)
 s=s.replace('</style></style>','</style>')
 # Preserve existing SEO work and internal article cluster.
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
 if '</style>' in s and '.ad-native' not in s:s=s.replace('</style>',CSS+'</style>',1)
 # Three ads distributed across the article's H2 structure, not stacked at the top.
 hs=list(re.finditer(r'</h2>',s,re.I))
 if hs:
  n=len(hs); idxs=sorted(set([max(0,n//4-1),max(0,n//2-1),max(0,3*n//4-1)]))
  ads=[NATIVE,BOX,WIDE]
  # Insert from the bottom so earlier positions remain valid.
  for idx,ad in reversed(list(zip(idxs,ads))):
   pos=hs[idx].end();s=s[:pos]+ad+s[pos:]
 # One Social Bar per page, no Popunder and no Smartlink.
 if SOCIAL not in s:s=s.replace('</body>',SOCIAL+'</body>',1)
 imgs=list(re.finditer(r'<img\b[^>]*>',s,re.I))
 for idx,m in reversed(list(enumerate(imgs))):
  tag=m.group(0)
  if 'decoding=' not in tag:tag=tag[:-1]+' decoding="async">'
  if idx>0 and 'loading=' not in tag:tag=tag[:-1]+' loading="lazy">'
  s=s[:m.start()]+tag+s[m.end():]
 s=s.replace('https://jawad123-creator.github.io/Negocios.IA/articulos/','/Negocios.IA/articulos/')
 p.write_text(s,encoding='utf-8')
