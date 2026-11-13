#!/usr/bin/env python3
"""Source monitor: fetch each record's official URL, detect change, flag for human review.
It NEVER edits facts. On change it only sets status='pending' + change_note, and writes monitor/report.json."""
import json,glob,hashlib,re,urllib.request,urllib.robotparser,urllib.parse,datetime
T=datetime.date.today().isoformat();SN='monitor/snapshots.json'
try: snap=json.load(open(SN))
except Exception: snap={}
rep={"run":T,"changed":[],"new":[],"manual_check":[],"errors":[]}
def get(u):
    p=urllib.parse.urlparse(u);rp=urllib.robotparser.RobotFileParser(f'{p.scheme}://{p.netloc}/robots.txt')
    try:
        rp.read()
        if not rp.can_fetch('NagrikSaathiMonitor',u): return None,'robots'
    except Exception: pass
    try:
        t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'NagrikSaathiMonitor/1.0'}),timeout=30).read().decode('utf-8','ignore')
        return re.sub(r'\s+',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>|<[^>]+>',' ',t,flags=re.S)).strip(),None
    except Exception as e: return None,str(e)[:80]
for f in sorted(glob.glob('content/*/*.json')):
    r=json.load(open(f,encoding='utf-8'));u=r.get('source_url')
    if not u: continue
    txt,err=get(u)
    if err=='robots': rep['manual_check'].append(r['slug']);continue
    if err: rep['errors'].append([r['slug'],err]);continue
    h=hashlib.sha256(txt.encode()).hexdigest()
    old=snap.get(u)
    if old is None: rep['new'].append(r['slug'])
    elif old!=h:
        rep['changed'].append(r['slug'])
        if r['status']=='verified': r['status']='pending'
        r['change_note']=f'Official source changed on {T}; re-verify before marking verified.'
        json.dump(r,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    snap[u]=h
json.dump(snap,open(SN,'w'),indent=1);json.dump(rep,open('monitor/report.json','w'),indent=1)
print(json.dumps(rep))
