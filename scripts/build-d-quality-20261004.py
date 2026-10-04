#!/usr/bin/env python3
"""Deterministic D quality assets. Run inside the worktree; never overwrite old assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import json, hashlib, io, math
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/d-quality-20261004'
OUT.mkdir(parents=True,exist_ok=True)
DER=ROOT/'media/derived'
AI=['ai-quick-risk-assessment','ai-risk-assessment-review','ai-similar-accident-alert','ai-subcontractor-safety']
SPECS=[(s,1,'top',f'product-{s}-scene-1280.webp',[480,768,1280,1600,2560]) for s in AI]+[
 ('wireless-emergency-broadcast',2,'top','product-wireless-emergency-broadcast-reference-white-20260912-707.webp',[480,768,1254]),
 ('compact-gas-detector',3,'detail-2','product-compact-gas-detector-diagram-453.webp',[480,768,1280,1812]),
 ('iot-small-tower-crane',4,'top','product-iot-small-tower-crane-reference-white-20260912-1280.webp',[480,768,1280,1600,2560]),
 ('emergency-signal-location',5,'top','product-emergency-signal-location-restored-20260913-1280.webp',[480,768,1280]),
 ('opening-open-close-sensor',6,'top','product-opening-open-close-sensor-scene-2560.webp',[480,768,1280,1600,1920,2560])]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save_new(p,data):
 if p.exists():
  if p.read_bytes()!=data:raise RuntimeError(f'Refusing to overwrite: {p}')
 else:p.write_bytes(data)
def encode(im,fmt,q=90,lossless=False):
 b=io.BytesIO()
 im.save(b,format=fmt.upper(),quality=q,**({'method':6,'lossless':lossless} if fmt=='webp' else {'speed':6,'subsampling':'4:4:4'}))
 return b.getvalue()
def deblock(im):
 # Small bilateral neighborhood smooths codec steps while weighting real edges down.
 a=np.asarray(im,dtype=np.float32); pad=np.pad(a,((1,1),(1,1),(0,0)),mode='edge')
 acc=np.zeros_like(a);den=np.zeros(a.shape[:2],np.float32)
 for dy in [-1,0,1]:
  for dx in [-1,0,1]:
   b=pad[1+dy:1+dy+a.shape[0],1+dx:1+dx+a.shape[1]]
   weight=np.exp(-np.mean((a-b)**2,axis=2)/(2*12**2)-(dx*dx+dy*dy)/(2*.8**2))
   acc+=b*weight[:,:,None];den+=weight
 return Image.fromarray(np.uint8(np.clip(acc/den[:,:,None],0,255).round()))
def helmet(im):
 a=np.asarray(im); candidate=(a.min(2)>=235)&((a.max(2).astype(int)-a.min(2))<=12)
 # Only neutral near-white pixels connected to the exterior qualify as background.
 m=Image.fromarray(np.uint8(candidate)*255)
 for pt in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]:ImageDraw.floodfill(m,pt,128)
 mask=np.asarray(m)==128;result=a.copy();result[mask]=255
 Image.fromarray(np.uint8(mask)*255).save(OUT/'helmet-background-mask.png')
 assert np.array_equal(a[~mask],result[~mask])
 (OUT/'helmet-mask-verification.json').write_text(json.dumps({'background_pixels':int(mask.sum()),'unchanged_product_pixels':int((~mask).sum()),'product_changed_pixels_before_encoding':0},indent=2))
 return Image.fromarray(result)
def diagram(original):
 # Original 453x255 geometry scaled four times. Original photographic inserts
 # remain source crops; no screen readings or physical parts are regenerated.
 sc=4; im=Image.new('RGB',(1812,1020),'white');d=ImageDraw.Draw(im)
 blue='#14678b';purple='#8a4a86';font='/System/Library/Fonts/AppleSDGothicNeo.ttc'
 def box(b):d.rounded_rectangle(tuple(round(v*sc) for v in b),radius=17*sc,outline=blue,width=3)
 def line(points,fill=blue,width=1):d.line([(round(x*sc),round(y*sc)) for x,y in points],fill=fill,width=max(2,round(width*sc)))
 def text(x,y,t,size=8,color='#252b30',anchor='la'):
  d.text((x*sc,y*sc),t,font=ImageFont.truetype(font,round(size*sc)),fill=color,anchor=anchor)
 def arrow(a,b):
  line([a,b]); ang=math.atan2(b[1]-a[1],b[0]-a[0]);pts=[b]
  for theta in [ang+2.72,ang-2.72]:pts.append((b[0]+10*math.cos(theta),b[1]+10*math.sin(theta)))
  d.polygon([(round(x*sc),round(y*sc)) for x,y in pts],fill=blue)
 def crop(b):
  tile=original.crop(b).resize(((b[2]-b[0])*sc,(b[3]-b[1])*sc),Image.Resampling.LANCZOS)
  im.paste(tile,(b[0]*sc,b[1]*sc))
 for b in [(4,8,116,111),(4,147,116,250),(279,1,437,78),(279,83,437,159),(279,165,437,242)]:box(b)
 crop((37,18,86,99));crop((346,17,426,64));crop((300,176,391,214))
 # Keep speaker photographic outline; remove only the old overprinted red callout.
 b=(370,90,427,157);tile=original.crop(b).convert('RGB');arr=np.array(tile)
 red=(arr[:,:,0]>arr[:,:,1]*1.30)&(arr[:,:,0]>arr[:,:,2]*1.20)&(arr[:,:,0]>140)
 # Red label is outside the speaker silhouette at the left margin.
 red[:,12:]=False;arr[red]=255
 tile=Image.fromarray(arr).resize((228,268),Image.Resampling.LANCZOS);im.paste(tile,(1480,360))
 for b in [(264,40),(264,118),(264,198)]:arrow((125,157 if b[1]==118 else 153 if b[1]==40 else 164),b)
 arrow((60,109),(60,144))
 d.ellipse((9*sc,96*sc,50*sc,138*sc),fill=blue)
 d.polygon([(44*sc,126*sc),(53*sc,134*sc),(45*sc,135*sc)],fill=blue)
 # LTE icon: original cloud + handset motif.
 d.rounded_rectangle((23*sc,108*sc,31*sc,117*sc),radius=2*sc,outline='white',width=3)
 line([(21,113),(19,110),(21,106),(24,106),(25,103),(30,103),(33,107),(35,109),(34,113)],'white',.6)
 text(29,121,'LTE',8,'white','ma')
 text(60,158,'스마트 안전장비',11,anchor='ma');text(60,172,'클라우드 서버',11,anchor='ma')
 # Smooth cloud outline follows the original icon silhouette.
 def curve(points):
  path=[]
  for p0,p1,p2,p3 in points:
   for t in np.linspace(0,1,30):
    path.append(((1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t*t*p2[0]+t**3*p3[0],(1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t*t*p2[1]+t**3*p3[1]))
  line(path,blue,2.3)
 curve([((49,226),(38,226),(39,215),(47,212)),((47,212),(42,207),(47,202),(53,208)),((53,208),(57,194),(74,198),(73,214)),((73,214),(83,216),(80,228),(72,226))])
 for y in [216,222,228]:
  d.rectangle((55*sc,y*sc,68*sc,(y+5)*sc),fill=blue)
  d.ellipse((55*sc,(y+2)*sc,68*sc,(y+7)*sc),fill=blue,outline='white',width=2)
  d.ellipse((55*sc,(y-2)*sc,68*sc,(y+2)*sc),fill=blue,outline='white',width=2)
 text(290,27,'안전종합상황판 &',7.7);text(290,38,'관리자 스마트폰',7.7)
 text(296,97,'현장 이동형스피커',7.3,purple)
 line([(347,108),(376,120)],purple,.65)
 text(329,123,'유독가스 위험',7.5,'#dc3343');text(329,132,'긴급대피하세요',7.5,'#dc3343')
 line([(345,148),(378,137)],purple,.65)
 text(363,216,'1초 이내 근로자에게',7.5,purple)
 text(363,228,'강력한 손목진동과 안전모 진동/부저음 전송',7.2,purple,'ma')
 im.save(OUT/'diagram-redrawn-master.png')
 return im
records={};summary=[]
for slug,num,section,source,widths in SPECS:
 page=ROOT/f'products/{slug}/index.html';before=page.read_text();snapshot=OUT/f'{slug}-before.txt'
 if not snapshot.exists():snapshot.write_text(before)
 old=DER/source;original=Image.open(old).convert('RGB');base=source.rsplit('-',1)[0]+'-20261004'
 method='Lanczos resize; UnsharpMask(radius=0.65, percent=40, threshold=3); no generative reconstruction'
 if num==3:master=diagram(original);method='4x deterministic redraw of original boxes, arrows, LTE/cloud icons and Korean labels; original photo inserts retained as Lanczos-upscaled crops'
 elif num==5:master=helmet(original);method='Exterior-connected neutral background mask to pure white; product pixels unchanged; full-size lossless WebP'
 elif num==6:master=deblock(original);method='3x3 bilateral deblocking (sigma spatial 0.8, range 12); high-quality re-encode under 1.5x original WebP bytes'
 else:
  w=max(widths);master=original.resize((w,round(original.height*w/original.width)),Image.Resampling.LANCZOS).filter(ImageFilter.UnsharpMask(radius=.65,percent=40,threshold=3))
 formats=['webp','avif'] if num in [1,3,6] else ['webp'];variants=[]
 for width in widths:
  im=master if width==master.width else master.resize((width,round(master.height*width/master.width)),Image.Resampling.LANCZOS)
  for fmt in formats:
   quality=90 if fmt=='webp' else 83
   lossless=num==5 and width==1280
   encoded=encode(im,fmt,quality,lossless)
   if num==6 and fmt=='webp' and width==2560:
    while len(encoded)>old.stat().st_size*1.5:
     quality-=1;encoded=encode(im,fmt,quality)
   p=DER/f'{base}-{width}.{fmt}';save_new(p,encoded)
   variants.append({'asset':'/'+str(p.relative_to(ROOT)),'width':im.width,'height':im.height,'bytes':len(encoded),'format':fmt,'quality':quality,'lossless':lossless,'sha256':sha(p)})
 final=next(v for v in variants if v['width']==max(widths) and v['format']=='webp')
 alt=BeautifulSoup(before,'html.parser').find(id=section).find('img')['alt']
 key=f'{slug}-d-{num}-20261004'
 records[key]={k:final[k] for k in ['asset','width','height','sha256']}
 records[key].update(alt=alt,reference='/'+str(old.relative_to(ROOT)),provenance='upscaled/cleaned from existing product photo; no new content',method=method,section=section,original_sha256=sha(old),variants=variants)
 summary.append({'key':key,'slug':slug,'section':section,'before':{'asset':records[key]['reference'],'width':original.width,'height':original.height,'bytes':old.stat().st_size},'after':final,'method':method})
 print(slug,original.size,'->',master.size,old.stat().st_size,'->',final['bytes'],flush=True)
(OUT/'records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
