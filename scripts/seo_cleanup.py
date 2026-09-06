from pathlib import Path
import re
BASE='/Negocios.IA/'
M={
'chatgpt-pequenos-negocios.html':('ChatGPT para pequeños negocios: 10 usos prácticos','10 formas prácticas de usar ChatGPT en un pequeño negocio para ahorrar tiempo, organizar tareas y mejorar procesos sin perder el control.'),
'automatizacion-make.html':('Automatización con Make para pequeños negocios','Aprende a automatizar tareas de un pequeño negocio con Make, probar el flujo y calcular si realmente compensa.'),
'ia-marketing-local.html':('IA para marketing local: guía práctica','Guía práctica para usar IA en marketing local, SEO local, Google Maps, contenido y reseñas para atraer clientes.'),
'chatgpt-vs-claude.html':('ChatGPT vs Claude: cuál elegir','Compara ChatGPT y Claude según la tarea, calidad, contexto, coste y utilidad para pequeños negocios.'),
'como-validar-una-idea-con-ia.html':('Cómo validar una idea de negocio con IA','Aprende a validar una idea de negocio con IA: problema, cliente, competencia, demanda y primeras pruebas.'),
'ia-para-pequenos-negocios-tareas.html':('15 tareas para usar IA en un pequeño negocio','15 tareas concretas en las que la IA puede ahorrar tiempo a un pequeño negocio, con ejemplos y criterios para decidir.'),
'calcular-roi-herramienta-ia.html':('Cómo calcular el ROI de una herramienta de IA','Aprende a calcular el ROI de una herramienta de IA teniendo en cuenta ahorro, coste, uso y resultados.'),
'errores-al-usar-ia-en-contenido.html':('7 errores al usar IA para crear contenido','Evita 7 errores habituales al usar IA para crear contenido: textos genéricos, datos inventados y falta de revisión.'),
'automatizar-tareas-sin-programar.html':('Cómo automatizar tareas sin programar','Guía práctica para identificar procesos repetitivos, elegir herramientas y automatizar tareas sin programar.'),
'como-elegir-herramienta-ia.html':('Cómo elegir una herramienta de IA para tu negocio','Aprende a elegir una herramienta de IA según tarea, coste, privacidad, integraciones, facilidad y retorno.'),
'ia-y-privacidad-datos-negocio.html':('IA y privacidad de datos en un negocio','Guía práctica para usar IA en un negocio reduciendo riesgos de privacidad y evitando compartir datos innecesarios.')}
for p in Path('articulos').glob('*.html'):
 if p.name not in M: continue
 s=p.read_text(encoding='utf-8'); title,desc=M[p.name]
 s=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',s,count=1,flags=re.S)
 s=re.sub(r'<meta name=["\']description["\'] content=["\'][^"\']*["\']',f'<meta name="description" content="{desc}"',s,count=1)
 s=re.sub(r'<meta property=["\']og:title["\'] content=["\'][^"\']*["\']',f'<meta property="og:title" content="{title}"',s,count=1)
 s=re.sub(r'<meta property=["\']og:description["\'] content=["\'][^"\']*["\']',f'<meta property="og:description" content="{desc}"',s,count=1)
 s=s.replace('</style></style>','</style>')
 s=s.replace('</p></div><div class="box">','</p><div class="box">')
 s=s.replace('</p></div><div class="use">','</p><div class="use">')
 s=s.replace('Afirmações que puedan perjudicar a terceros','Afirmaciones que puedan perjudicar a terceros')
 # Remove all ad formats and ad-network scripts. The dedicated ad placement step adds the controlled set afterwards.
 s=re.sub(r'<div class="ad-native">.*?</div>|<div class="ad-300">.*?</div>|<div class="ad-responsive[^>]*>.*?</div>|<div class="smartlink-box">.*?</div>','',s,flags=re.S)
 s=re.sub(r'<script[^>]+(?:profitableratecpmnetwork|highrevenueformat\.com)[^>]+></script>','',s,flags=re.S)
 imgs=list(re.finditer(r'<img\b[^>]*>',s,re.I))
 for idx,m in reversed(list(enumerate(imgs))):
  tag=m.group(0)
  if 'decoding=' not in tag: tag=tag[:-1]+' decoding="async">'
  if idx>0 and 'loading=' not in tag: tag=tag[:-1]+' loading="lazy">'
  s=s[:m.start()]+tag+s[m.end():]
 s=s.replace('https://jawad123-creator.github.io/Negocios.IA/articulos/','/Negocios.IA/articulos/')
 p.write_text(s,encoding='utf-8')
