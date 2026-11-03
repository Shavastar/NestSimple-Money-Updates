from pathlib import Path
import ast,sys,importlib,zipfile,json,hashlib,tempfile,shutil
base=Path('work');sys.path.insert(0,str((base/'current-source').resolve()))
for name in ('app','income_dashboard','list_filters','control_size','program_updates'):
 ast.parse((base/'current-source'/(name+'.py')).read_text(encoding='utf-8-sig'),feature_version=(3,10));importlib.import_module(name)
with zipfile.ZipFile(base/'NestSimple-Money-v1.2.22.nsmupdate') as z:
 m=json.loads(z.read('manifest.json'));assert z.testzip() is None
 assert set(z.namelist())=={'manifest.json','What Changed.html'}|{'payload/'+n for n in m['files']}
 for n,e in m['files'].items():assert hashlib.sha256(z.read('payload/'+n)).hexdigest()==e['new']
 import program_updates as u
 with tempfile.TemporaryDirectory(dir=base) as d:
  root=Path(d)/'app';shutil.copytree(base/'installed-source',root)
  with zipfile.ZipFile(base/'NestSimple-Money-v1.2.21.nsmupdate') as old:
   for n in old.namelist():
    if n.startswith('payload/'):(root/n[8:]).write_bytes(old.read(n))
  folder,_=u.prepare(base/'NestSimple-Money-v1.2.22.nsmupdate',root);u.apply(root,folder)
  assert all(u.digest(root/n)==e['new'] for n,e in m['files'].items())
print('PASS Python 3.10 syntax, imports, package inventory/hashes and previous v1.2.21->v1.2.22 compatibility/apply')

