from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent/'current-source'))
from budget_hierarchy import income_parent,INCOME_GROUPS,ordered
from chart_hierarchy import rows_for
from finance import INCOME_CATEGORIES
assert income_parent('Salary & wages')=='Income'
assert income_parent('Refunds')=='Income'
assert income_parent('Pension')=='Benefits'
assert income_parent('Government benefits')=='Benefits'
for c in ('Interest & dividends','Gifts received','Other income'):assert income_parent(c)==c
items=[(c,(100,)) for c in INCOME_CATEGORIES]
spec={'_category_chart':True,'_group_map':{c:income_parent(c) for c in INCOME_CATEGORIES},'_group_order':list(INCOME_GROUPS)}
for expanded in (set(),set(INCOME_GROUPS)):
 rows=rows_for(spec,items,expanded);assert sum(r[1][0] for r in rows)==len(items)*100
 assert sum(r[0]=='Interest & dividends' for r in rows)==1
assert [g for g,rows in ordered(items,True)]==list(INCOME_GROUPS)
app=(Path(__file__).parent/'current-source/app.py').read_text();assert 'currency_selector(menu,self)' in app
print('PASS Income and Benefits hierarchy, standalone categories, expanded pie totals and currency selector placement')

