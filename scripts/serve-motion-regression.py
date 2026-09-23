"""Local-only browser regression probe; never injected into release HTML."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PROBE='''<script>
document.addEventListener('DOMContentLoaded',()=>{
const output=document.createElement('pre');output.id='motion-check';output.style.cssText='position:fixed;bottom:0;left:0;z-index:99999;background:white;color:black;font:11px monospace;padding:8px;max-width:95vw;max-height:90px;overflow:auto';document.body.append(output);
const targets=[...document.querySelectorAll('main h2')].filter(h=>!h.closest('[data-scroll-flow],.solar-story,.home-families,.editorial-hero,.page-head,[hidden]'));
const report={checks:[],failures:[]};function check(label){const pending=targets.filter(h=>h.getBoundingClientRect().top>innerHeight);const bad=pending.filter(h=>Number(getComputedStyle(h).opacity)>.001);report.checks.push({label,pending:pending.length,visible:bad.length});if(bad.length)report.failures.push({label,titles:bad.map(h=>h.textContent)});output.textContent=JSON.stringify(report)}
setTimeout(()=>{check('initial');ScrollTrigger.refresh();requestAnimationFrame(()=>{check('refresh');output.dataset.done='true'})},1200);
});</script>'''
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def do_GET(self):
  if self.path.startswith('/__motion__/'):
   route=self.path.split('?')[0].removeprefix('/__motion__');p=ROOT/route.lstrip('/')/'index.html'
   if not p.resolve().is_relative_to(ROOT) or not p.is_file():
    self.send_error(404);return
   text=p.read_text().replace('</head>',PROBE+'</head>',1);b=text.encode();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
  else:super().do_GET()
 def log_message(self,*a):pass
if __name__ == '__main__':
 print('Open http://127.0.0.1:8779/__motion__/products/co2-temp-humidity/ at 1280x900; expect pending > 0 and visible = 0 in both checks.')
 ThreadingHTTPServer(('127.0.0.1',8779),Handler).serve_forever()
