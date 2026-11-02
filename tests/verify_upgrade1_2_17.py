from pathlib import Path
import sys,tempfile,shutil,hashlib
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
import program_updates as u
base=Path(__file__).parent
def snapshot(root):
 return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and 'program-update-backups' not in p.parts}
with tempfile.TemporaryDirectory(dir=base) as temporary:
 root=Path(temporary)/'app';shutil.copytree(base/'installed-source',root)
 shutil.copy2(base/'v198/payload/STYLE_GUIDE.md',root/'STYLE_GUIDE.md')
 (root/'household.sqlite3').write_bytes(b'household preservation sentinel')
 (root/'settings.json').write_bytes(b'personal settings sentinel')
 before=snapshot(root)
 folder,manifest=u.prepare(base/'NestSimple-Money-v1.2.17.nsmupdate',root)
 real_replace=u.replace_file;calls=[0]
 def fail_once(source,target):
  calls[0]+=1
  if calls[0]==2:raise OSError('simulated replacement failure')
  return real_replace(source,target)
 with patch.object(u,'replace_file',side_effect=fail_once):
  try:u.apply(root,folder)
  except u.UpdateInstallError:pass
  else:raise AssertionError('Failure was not surfaced')
 assert snapshot(root)==before,'Failed update did not restore original program'
 u.apply(root,folder)
 for name,entry in manifest['files'].items():assert u.digest(root/name)==entry['new']
 assert (root/'household.sqlite3').read_bytes()==before['household.sqlite3']
 assert (root/'settings.json').read_bytes()==before['settings.json']
print('PASS real v198->v1.2.17 package preparation, backup, injected failure rollback, successful apply and household/settings preservation')

