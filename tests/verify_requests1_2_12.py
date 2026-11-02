from pathlib import Path
import sys,tempfile
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from currency_menu import currency_label,DISPLAY_NAMES
from currencies import CURRENCIES
from finance import Store
from budget_print import budget_report_data,create_budget_pdf
assert set(DISPLAY_NAMES)==set(CURRENCIES)
assert currency_label('CAD')=='  Canadian Dollar'
with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
 store=Store(folder);store.backup_enabled=False
 app=SimpleNamespace(store=store,month=SimpleNamespace(get=lambda:'2026-11'),profile={'household':'Budget print check'})
 d=budget_report_data(app)
 assert d['headings'][0]=='Category'
 assert set(r[0] for r in d['rows'])==set(r[0] for r in store.budget_rows('2026-11'))
 assert len(d['rows'])>10
 path=Path(__file__).parent/'budget-all-categories1_2_12.pdf';create_budget_pdf(app,path)
 store.db.close()
source=(Path(__file__).parent/'current-source/testing_ui.py').read_text(encoding='utf-8')
assert "('<ButtonPress-1>','<FocusIn>')" in source and "app.unbind(name,ident)" in source
print('PASS currency names and spaces, full zero-budget category list, paginated budget PDF, outside-focus dismissal hooks and cleanup')

