from pathlib import Path
import sys,zipfile,tempfile,importlib.util,json,hashlib,subprocess
from unittest.mock import patch
b=Path(__file__).parent.resolve()
def overlay(root,p):
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.startswith('payload/'):
    target=root/n[8:];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(n))
with tempfile.TemporaryDirectory(dir=b) as t:
 root=Path(t)/'Remote user'/'NestSimpleMoney';root.parent.mkdir(parents=True);__import__('shutil').copytree(b/'installed-source',root)
 # Retain untouched base runtime files; rebuild every candidate-controlled file
 # from the older published payloads so newer modules cannot mask omissions.
 with zipfile.ZipFile(b/'NestSimple-Money-v1.2.35.nsmupdate') as z:
  for name in json.loads(z.read('manifest.json'))['files']:(root/name).unlink(missing_ok=True)
 for p in (b/'gate-fixture/packages/NestSimple-Money-v1.0.137.nsmupdate',*sorted((b/'historical183').glob('*.nsmupdate')),b/'NestSimple-Money-v1.0.183.nsmupdate'):overlay(root,p)
 sys.path.insert(0,str(root));spec=importlib.util.spec_from_file_location('old183',root/'program_updates.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 assert old.CURRENT_VERSION=='1.0.183';assert not (root/'budget_hierarchy.py').exists()
 try:old.prepare(b/'NestSimple-Money-v1.2.34.nsmupdate',root)
 except ValueError as e:assert 'budget_hierarchy.py' in str(e);print('REPRODUCED exact v1.0.183 failure:',e)
 else:raise AssertionError('Old failure not reproduced')
 for name in ('household/finances.sqlite3','profile.json','testing/edits.txt','attachments/document.txt'):
  p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'data preservation sentinel')
 def snapshot():return {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file() and 'program-update-backups' not in p.parts}
 before=snapshot();folder,m=old.prepare(b/'NestSimple-Money-v1.2.35.nsmupdate',root)
 replace=old.replace_file;calls=[0]
 def fail_once(source,target):
  calls[0]+=1
  if calls[0]==4:raise OSError('Injected failure')
  return replace(source,target)
 with patch.object(old,'replace_file',side_effect=fail_once):
  try:old.apply(root,folder)
  except OSError:pass
  else:raise AssertionError('Expected failure')
 assert snapshot()==before,'Rollback changed original files'
 old.apply(root,folder)
 for name,e in m['files'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==e['new'],name
 for name,data in before.items():
  if name.startswith(('household/','testing/','attachments/')) or name=='profile.json':assert (root/name).read_bytes()==data
 result=subprocess.run([sys.executable,'-c','import sys;sys.path.insert(0,sys.argv[1]);import app,program_updates;assert program_updates.CURRENT_VERSION=="1.2.35";print("PASS upgraded app import and version")',str(root)],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 print(result.stdout.strip());print('PASS original v1.0.183 updater -> v1.2.35,203 exact payload files, missing dependency added, injected failure rollback, household/profile/testing/attachments preserved')
