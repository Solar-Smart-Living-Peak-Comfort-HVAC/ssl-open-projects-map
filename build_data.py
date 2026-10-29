import json,re,html,sys,time,urllib.request,urllib.parse,os
t=open(sys.argv[1]).read();s=t.find('[');L=json.loads(t[s:t.rfind(']')+1])
cc=json.load(open('/workspace/cc_cache.json'))
gc_path='/workspace/ssl-map/geocache.json'; gc=json.load(open(gc_path)) if os.path.exists(gc_path) else {}
def txt(h): h=re.sub(r'<br ?/?>|</(div|p|tr|td|th|li)>','\n',h or ''); return re.sub(r'[ \t\xa0]+',' ',html.unescape(re.sub('<[^>]+>',' ',h)))
def geo(q):
  if q in gc: return gc[q]
  u='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'json','limit':1,'countrycodes':'us','viewbox':'-107.5,32.6,-105.8,31.3'})
  r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'SSL-project-map/1.0 (luke internal)'})));time.sleep(1.1)
  gc[q]=[float(r[0]['lat']),float(r[0]['lon'])] if r else None; json.dump(gc,open(gc_path,'w')); return gc[q]
out=[]
for p in L:
  grp=(p.get('project_group') or {}).get('name','')
  if 'internal' in grp.lower() or p['name'].startswith('X-'): continue
  d=txt(p.get('description')); lines=[x.strip() for x in d.split('\n') if x.strip()]
  ref=d.find('Referral'); main=d[:ref] if ref>0 else d
  ph=re.search(r'\(?\b\d{3}\)?[\s.-]*\d{3}[\s.-]\d{4}\b',main); phone=ph.group(0).strip() if ph else None
  m=re.search(r'projects/(\d+)',p.get('company_cam_link') or ''); ccid=m.group(1) if m else None
  c=cc.get(ccid) if ccid else None
  addr=lat=lng=None; src=None
  if c and c.get('address') and c['address'].get('street_address_1'):
    a=c['address']; addr=f"{a['street_address_1']}, {a.get('city') or ''}, {a.get('state') or ''} {a.get('postal_code') or ''}".strip()
    co=c.get('coordinates') or {}
    if co.get('lat'): lat,lng=co['lat'],co['lon']; src='companycam'
  if not addr:
    for x in lines[:6]:
      if re.match(r'^\d+ .+,\s*[A-Za-z .]+,\s*(TX|NM)\b',x): addr=x; break
  if not addr:
    mm=re.search(r' - (\d+ [^-]+?) - ',p['name'])
    if mm: addr=mm.group(1).strip()+', El Paso, TX'
  if addr and lat is None:
    try: g=geo(addr)
    except Exception as e: g=None
    if g: lat,lng=g; src='nominatim'
  st=p.get('status') or {}
  fl=p.get('fsm_link') or ''; fl=fl if 'fsm.zoho.com' in fl else None
  wo=p.get('fsm_wo_number'); wo=wo if wo and wo.strip('-') else None
  out.append(dict(prj=p.get('key'),id=p['id'],name=re.sub(r'\s+',' ',p['name']),stage=st.get('name',''),color=st.get('color_hexcode') or '#999',
    group=grp,address=addr,lat=lat,lng=lng,source=src,phone=phone,
    zoho=f"https://projects.zoho.com/portal/sslproject1#project/{p['id']}/dashboard",
    companycam=f"https://app.companycam.com/projects/{ccid}" if ccid else None,fsm=fl,fsm_wo=wo,podium=None,
    outside=bool(lat and not (31.3<=lat<=32.6 and -107.5<=lng<=-105.8))))
json.dump({'generated':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'projects':out},open('/workspace/ssl-map/projects.json','w'),indent=1)
import collections;print(len(out),sum(1 for o in out if o['lat']),sum(1 for o in out if not o['address']),sum(1 for o in out if o['address'] and not o['lat']),sum(o['outside'] for o in out),sum(1 for o in out if o['phone']))
