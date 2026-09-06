from pathlib import Path
import re,json
BASE='https://jawad123-creator.github.io/Negocios.IA/'
AD='<div class="ad-300" aria-label="Publicidad"><script>atOptions={"key":"f177569624c6dd37ca61725706854f70","format":"iframe","height":250,"width":300,"params":{}};</script><script src="https://www.highrevenueformat.com/f177569624c6dd37ca61725706854f70/invoke.js"></script></div>'
CSS='<style>.related-content{margin-top:52px;padding-top:28px;border-top:1px solid #ffffff1a}.related-content li{margin:10px 0}.ad-300{width:300px;min-height:250px;margin:34px auto;display:flex;align-items:center;justify-content:center;overflow:hidden}details{background:#121a2e;border:1px solid #ffffff1a;border-radius:10px;padding:15px 18px;margin:12px 0}summary{cursor:pointer;font-weight:700}</style>'
files=sorted(Path('articulos').glob('*.html')); names=[p.name for p in files]
for i,p in enumerate(files):
 s=p.read_text(encoding='utf-8')
 # Shorten titles while preserving the primary topic.
 mt=re.search(r'<title>(.*?)</title>',s,re.S)
 if mt:
  t=re.sub(r'\s*\|\s*Negocios\.IA$','',mt.group(1)).strip()
  if len(t)>60:t=t[:57].rsplit(' ',1)[0]+'…'
  s=s[:mt.start(1)]+t+s[mt.end(1):]
 # Keep descriptions useful and below the usual truncation range.
 md=re.search(r'(<meta name="description" content=")([^"]*)(")',s)
 if md and len(md.group(2))>155:
  d=md.group(2)[:152].rsplit(' ',1)[0]+'…';s=s[:md.start(2)]+d+s[md.end(2):]
 # Remove the old aggressive ad system, smartlinks and extra external scripts.
 s=re.sub(r'<div class="ad-native">.*?</div>|<div class="ad-300">.*?</div>|<div class="ad-responsive[^>]*>.*?</div>|<div class="smartlink-box">.*?</div>','',s,flags=re.S)
 s=re.sub(r'<script[^>]+(?:profitableratecpmnetwork|highrevenueformat\.com)[^>]+></script>','',s,flags=re.S)
 # Add image decoding hints.
 s=re.sub(r'<img\b[^>]*>',lambda m:m.group(0) if 'decoding=' in m.group(0) else m.group(0)[:-1]+' decoding="async">',s,flags=re.I)
 # Repair Article schema with image + publisher/logo when JSON-LD is present.
 def schema(m):
  try:o=json.loads(m.group(1))
  except:return m.group(0)
  arr=o if isinstance(o,list) else [o];changed=False
  for x in arr:
   if isinstance(x,dict) and x.get('@type')=='Article':
    im=re.search(r'<img[^>]+src=["\']([^"\']+)',s)
    if im:x['image']=im.group(1)
    x['publisher']={'@type':'Organization','name':'Negocios.IA','url':BASE,'logo':{'@type':'ImageObject','url':BASE+'favicon.svg'}};changed=True
  if not changed:return m.group(0)
  return '<script type="application/ld+json">'+json.dumps(o if isinstance(o,list) else arr[0],ensure_ascii=False,separators=(',',':'))+'</script>'
 s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,s,flags=re.S)
 if '</style>' in s and 'class="related-content"' not in s:s=s.replace('</style>',CSS+'</style>',1)
 # Build a real article cluster: link to three other articles.
 if 'class="related-content"' not in s:
  others=[names[(i+j)%len(names)] for j in (1,2,3)]
  lis=''.join(f'<li><a href="{BASE}articulos/{x}">{re.sub("[-]", " ", x[:-5]).replace("ia ","IA ").title()}</a></li>' for x in others)
  block=f'<section class="related-content"><h2>Artículos relacionados</h2><p>Continúa con estas guías para profundizar y aplicar lo aprendido:</p><ul>{lis}</ul></section>'
  s=s.replace('</main>',block+'</main>',1)
 # Add practical FAQ content where the page has none.
 if 'id="faq"' not in s:
  h1=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
  topic=re.sub('<.*?>','',h1.group(1)).strip() if h1 else 'este tema'
  faq=f'<section id="faq"><h2>Preguntas frecuentes</h2><details><summary>¿Por dónde empezar con {topic.lower()}?</summary><p>Empieza por una necesidad concreta, prueba el proceso con un caso real y mide el resultado antes de ampliarlo.</p></details><details><summary>¿Cómo saber si funciona?</summary><p>Define una métrica antes de empezar y compara el resultado con la situación anterior. El objetivo es mejorar un proceso, no simplemente usar una herramienta.</p></details><details><summary>¿Qué conviene revisar antes de aplicarlo?</summary><p>Comprueba datos, costes, privacidad, limitaciones de la herramienta y el impacto real sobre el negocio.</p></details></section>'
  s=s.replace('</main>',faq+'</main>',1)
 # One ad per article, placed after the second H2; no popup/smartlink.
 if 'aria-label="Publicidad"' not in s:
  hs=list(re.finditer(r'</h2>',s,re.I))
  if hs:
   pos=hs[min(1,len(hs)-1)].end();s=s[:pos]+AD+s[pos:]
 p.write_text(s,encoding='utf-8')
