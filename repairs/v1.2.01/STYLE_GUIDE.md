# NestSimple Money Style Guide

These are project rules for implementation and review. Keep this guide in step with approved shared designs. Add a rule when a common function or design is established; do not invent new conventions without agreement.

## Scope and review
- Make only requested changes. Reuse established controls and behaviour.
- Tell Brian when a change makes a feature or control redundant. Remove it only when authorised.
- Keep updates focused and explain what changed and how it was checked. Do not claim Windows visual verification without running it.
- Preserve personal data and testing edits. Never reset a household during a program update.

## Branding
- Use the approved NestSimple Money house-and-coin logo, title NestSimple Money, and tagline Home Accounting Made Simple.
- Installer branding uses a horizontal group: approved logo on the left; NestSimple and Money on two lines to its right; tagline below. The tagline is larger and bold but smaller than the title. Installer screens must display the same logo, title and tagline as the main menu. Keep the logo proportional and legible; never stretch it to fit a banner.
- Application/taskbar icons use the approved transparent mark without text.

## Colour and typography
- Each section keeps its assigned menu, banner and subpage colours. Main banners use the darker section colour; subordinate areas use lighter matching colours.
- Information cards have white backgrounds. Overview uses light tan.
- Green means healthy progress or paid; true red means a problem or overspending. Section identity and status colours have separate purposes.
- Capitalise main words in titles. Keep household branding prominent. Avoid repeated page titles.

## Icons and commands
- The same action uses the same approved icon throughout the app. Icon-only controls have hover text and keyboard access.
- Buttons act on a single click. Record lists select on a single click and open details on a double click.
- Previous/Next use compact triangle icons without button borders, on either side of the period field.
- Question-mark help buttons are removed throughout the app. Retain Help navigation, setup guides and hover labels.

## Navigation
- Back goes up one level; Close returns to the section main page. Use the established title-bar icons.
- Prefer subpages to popups for records, entry and management. Testing is an explicitly requested popup with tabs.
- Main menu has no scrolling. Pages and constrained panels scroll when needed.

## Entry and details
- Use compact Bill Entry as the reference: inputs left, document preview right, separate contact tab, document commands top and Save bottom.
- Dates and short choices should use only the needed width. Description is optional and two lines where requested.
- Bill Details actions: Make Bill Payment, Open Original, Edit, Delete. Paid records retain View Payment.
- Bill information is left; Original and Contact tabs are right and only slightly taller than the information, with internal scrolling as needed. No explanatory text below the original image.
- Preview clicks open the original file in its default viewer.

## Tables and searches
- Fit tables within their containers with equal left/right inner margins. Avoid horizontal scrolling on full-page lists.
- Give Supplier/Description spare width. Amount should fit 1000000.00. Dates, status and repeats use content-sized columns.
- Centre every header, including the title-plus-sort-arrow group. Currency values align right; dates align centre.
- Header click toggles ascending/descending; show a crisp green triangle with a white outline directly after the title, separated by a small space. Never enlarge header height repeatedly to resize an arrow.
- Status sorts Overdue, Upcoming, Paid on its first click. Status (Days) uses a coloured box, space, status text and day count.
- Repeats uses its existing icon and Once, Monthly or Yearly plus the remaining count when defined. Do not add Ongoing or an extra icon column.
- Search is case-insensitive, supports Boolean terms and existing spelling tolerance. Search uses the single-handle magnifying glass.
- Search clears using a large blue X inside the right edge of the field, with Clear search hover text.
- Supplier selectors are compact and use the section’s light background colour with black text when closed; the open list is wider with black text on white. Use All Suppliers and no redundant external label.

## Bills calendar
- One row, equal control heights: Add Schedule, Previous icon, date/period field, Next icon, All Suppliers, search field with clear X, Search button.
- Choose a month or year in the period field. Calendar dates have no command icons; scheduled dates are marked. Keep date cells compact and lists within the page.

## Accounts and money
- Bill payment sources: Chequing, Savings, Cash and Credit Card. Loan and Mortgage are debts, not payment sources.
- Account Type includes Mortgage and Loan. Debt opening values are negative; totals show Assets minus Debts.
- Linked loans show Payments to Go based on recorded balance and planned payment; do not imply interest/amortisation calculations that are not implemented.
- Variable budget suggestions use historical averages; fixed suggestions use the highest actual. Follow the existing rounding rules.

## Printing and installer
- Non-entry print pages omit controls and backgrounds. Card reports follow the approved Overview layout; long lists use full-width continuation pages without blanks.
- Calendar print shows the filtered list and a title naming its month or year, without navigation controls.
- Installer chooses the program folder, shows file progress, then displays completion in the same window without a success popup.
- Keep native Close visible. Show Files sits beside Close in the bottom button row and opens the installed-file list on request.
- Use E:\Documents\NestSimple-Money-Windows\temp for updater staging, not Windows Documents or Windows temporary storage.

## Testing window
- Testing sits immediately above Contacts and replaces the redundant Open Sample Data menu button.
- Version History navigation uses icons only: Previous moves to an older (lower) version; Next moves to a newer (higher) version. Keep hover labels and keyboard access. The version list is ordered newest first with previous/version/next controls and full available change notes. Preserve notes exactly; label unavailable historical notes rather than inventing them.
- Style Guide shows this shared rulebook. Update it when an approved common function or design is added.

- The Style Guide tab uses two-thirds of its width for the rules and one-third for a scrollable visual reference of graphical styles. Maintain the reference when approved shared graphical styles change.

- Installer progress and completion use branding on the left with information and actions on the right. Directory selection uses the same left branding panel and right content column, with folder controls in the right column. Centre the tagline within the navy branding block; keep the approved logo left and two-line title beside it. Keep the native header and bottom button row fixed. The white content page fills the client width from the header bottom to the footer.

- Stages within one process must keep identical page geometry, branding artwork and dimensions, margins, content alignment and footer position. File installation and completion share the same page template and layout; do not switch to an enlarged finish sidebar.

- Bills printing uses the approved card-and-chart report style: total, paid, unpaid and upcoming summary cards, a status pie chart, supplier bars and the displayed bill list. Longer lists continue at readable sizes with repeated headings. Never print page navigation controls or icons.

- Approved installer reference: Brian’s completion-page screenshot (30 October 2026). Use its navy branding panel, centred tagline, white content area, fixed header and native bottom button row on all installer pages. Reuse the same bitmap and shared rectangle definitions; change only the page-specific content.

- Installer navy panel must reach the left client edge and header bottom. Information area is explicitly white, with a 10-dialog-unit gutter between the navy column and text. Keep the native footer unchanged.

- Version History displays changes as numbered points. Design/style changes include a labelled example image; distinguish reference examples from screenshots of that historical version.

- Installer uses one persistent branding panel owned by the main dialog, so changing pages cannot hide the logo. Use the approved screenshot artwork. White page background must reach the header and right client edge; do not fake this with overlapping inset background panels.

- Show the installer window before any staging disk writes. Make the current native page visible before raising the persistent branding panel, and repaint it after each stage transition.

- Bills Calendar columns: Date, Description, Amount, Type. Type shows a coloured box, a space and its text: red Unpaid, green Paid, yellow Upcoming. Preserve record navigation from the indicator.

- Never place text against a window, page, card or panel edge. Always leave inner padding on all sides. Installer information titles are bold, with one blank line above them and consistent left/right padding on every stage.

- Preserve the approved installer appearance while investigating performance. Avoid diagnostic helper loading before the first window. Compare startup changes against v1.0.92-94; distinguish source findings from measured Windows timings.

- Do not extract or load an unused header logo when the shared left branding panel supplies the approved identity. Keep the selected native dialog resource unchanged.

- Transactions print uses the same card-and-chart layout as Bills, with Transactions colours, Income/Expenses/Net Income/Total Activity cards, an income/expense pie, spending-category bars and the complete displayed list.

- Income and Bills calendar printouts use summary cards, pie/bar charts and the displayed filtered list, with month/year in the heading and no navigation controls. Add sample data once to existing fictional households; never replace testing edits or seed personal households.

- Income and Bills calendar toolbar: Add Schedule, By Month/By Year toggle, Previous icon, plain period field, Next icon, supplier/account filter and search. Period fields have no dropdown; print follows the chosen mode.

- Installer first-page startup performs no staging writes or bitmap extraction. Branding is embedded as an EXE resource; staging starts only after Install. Cache shared font/DPI coordinate conversion rather than allocating structures for every control. Retain integrity checks and do not bypass Windows security checks.

- Install Update sits directly below Testing. Select a .nsmupdate data package, review its version, then Apply Update and Restart. Use the already-installed updater, validate paths/hashes/compatibility, back up program files, close all registered app windows before replacement, restore previous files on failure and reopen the current household. Never replace household data or profiles.
- Each Budget card-page prints its own data in the shared cards-and-charts style: Income sources, Savings categories, Expenses categories and Charts. Main Budget print summarizes the four cards. Keep complete category tables and readable continuation pages; do not route every subpage to the overall report.

- Install Update opens a subpage that checks the approved Shavastar/NestSimple-Money-Updates GitHub repository. Show version and numbered release notes, download in the background, verify package size and SHA256, then reuse the existing review/apply/backup/restart flow. Keep Choose Update File as a manual fallback. Never upload household data or include GitHub credentials in the desktop application.

- Main menu Testing and Update share one row above Contacts, Testing on the left and Update on the right. Use equal widths; the combined row aligns with the main menu buttons. Update retains the online check and manual file selection. This replaces the separate Install Update row.

- Budget Savings cards distinguish planned savings from recorded actuals. Show the planned total prominently, recorded savings, amount left and the category breakdown. Savings plan history and printouts use the same underlying budgets and actual records; never fabricate savings transactions or treat a plan as money already saved.

- Budget summary headers use Planned Savings to match the Savings card. Budget main cards show a clearly labelled total with supporting counts and relevant breakdowns beneath it; keep recorded money distinct from plans.

- Transactions and Income main-page action commands use one row. Transactions has no page help button. Income uses compact white Overview-style summary cards that reflect the displayed records, including active period, account and search filters. Keep all actions reachable through the page viewport at small window sizes.


- Always design tables, fields, cards and action rows to fit the available page width without horizontal scrollbars. Resize columns, prioritise meaningful text, wrap card text and use compact icon controls with hover labels when needed; preserve vertical scrolling for long content. Align action buttons with the left edge of the associated table columns and keep equal table margins. Income and Transactions use this shared alignment.

- Main-page information cards share the Income card style: white background, thin border, 12-pixel inner padding, bold 11-point titles in the section sub-banner colour, blue 19-point totals and smaller supporting text. Wrap content to fit. Align action rows, cards and table content on the same left edge; preserve card data and actions.


- Main-page information cards share the Income card style: white background, thin border, 12-pixel inner padding, bold 11-point titles in the section sub-banner colour, blue 19-point totals and smaller supporting text. Wrap content to fit. Align action rows, cards and table content on the same left edge; preserve card data and actions.

- All pie charts use solid-colour slices without outlines or separator strokes, on screen and in printed reports. Preserve colours, labels and legends.

- All notebook tabs use the selected tab padding in every state, keeping selected and unselected tabs the same height across pages. Preserve section colours.

- Pie Chart and Bar Chart are sibling tabs beside Manage; do not wrap them in a redundant Pie & Bar Charts tab. Income and Savings reports include labelled 12-month trend graphs with exact values, preserving detailed records and distinguishing planned from recorded savings.

- Income and Savings trend graphs and histories cover 12 months ending in the selected month. Trend Graph is a sibling chart tab. Fill only blank fictional sample contact fields once; preserve existing values and personal households.

- List-filter buttons, period fields, selectors and search entries share a common rendered height; the blue clear X fits inside the search entry. Put Previous/Next arrow icons beside period fields. Accounts summary cards use compact padding and the main table fills the available viewport at standard startup size; long account lists scroll internally. Align Income action rows with their table content, including Calendar, Pay Day and Budget Income lists.

- Overview exception: only card titles use the section colour; all other page text, totals, account buttons and chart labels use black. My Accounts buttons fill the card width with equal padded left/right margins. Preserve chart and progress colours.

- Online update downloads show a percentage and byte progress bar on the Download Update page. Stay on that page through download and package verification; open installation review only after successful verification. Disable competing download/file commands while busy, and keep failures on the download page with retry available.

- Shared list period selectors show the active All Dates, Month or Year mode. Workspace action rows align with table content at the same inset. All installed-version displays read the updater version. Preserve the approved Bills graph table.

- Bills Trend Graph initially sorts Unpaid, Upcoming, Paid; retain later user-selected column and direction across redraws, navigation and launches.

- Summary cards use shared title, total and supporting-text styles, content-driven heights and equal heights within each row. Income has no fixed minimum card height. Retain compact Accounts cards to leave room for the list, Overview black-text rules, section colours, card data and actions.
- Preserve both approved calendar styles: full calendar subpages for schedules and records, and popup date pickers for filling date fields on detail and entry pages.

- Update download progress uses medium blue (#3B82C4), independent of the Windows theme.

- Account (including Loan/Mortgage), Contact and Transaction entry/edit forms use section subpages with shared Save and Cancel commands at the bottom, Back to the prior page and Close to the section main page. Preserve validation, contacts and attachments. Shared record lists retain filters, sorting, selection and scroll position on return; distinguish No Records Entered from No Records Match These Filters and offer Clear Filters for filtered empty results.

- Accounts action rows: Add Account, Edit Account, Transfer Money, Transfer History and Add Loan first; Import Statement, Quick Entry, Check Statement and Assign Older Records second. Check Statement opens a section subpage defaulting to the first Chequing account. Contact-detail Linked Records uses four visible rows with internal scrolling.

- Transfer Money and Transfer History use Accounts subpages. Transfer entry uses shared Save, Cancel, Back and Close; history retains edit, delete and double-click details.

- Memo entry fields use a wider five-line text area with word wrapping and a vertical scrollbar. Preserve memo contents when creating and editing records.

- Back and Close navigation controls and their containers match the surrounding subtitle or page background, without white boxes; preserve icons, hover labels and navigation behaviour.

- Shared record lists show active period, account/supplier, search and displayed record count. Capture return state before destroying list widgets. Unpaid sorts with Overdue before Upcoming and Paid; bills due today are red Unpaid. Keep the Bills graph table and calendar styles unchanged.

- All closed dropdown fields use the active section’s light background colour with black text, including Bills suppliers. Preserve opened list backgrounds and selection colours; disabled fields retain their disabled appearance.

- Accounts, Income and Transactions main reports use displayed records and sort order, show active filters, and calculate cards/charts from those records. Use white cards, section-coloured headings and black body text, with wrapped readable list rows and repeated headings/page numbers on continuation pages. Income retains a separate 12-month recorded-income history following account/search filters; label its history range and exact monthly values.

- Budget and Savings Goals reports follow the current page and displayed list filters/order. Distinguish planned savings, rollover availability, recorded savings and reserved goal allocations. Goal detail includes displayed payment history and labels undated opening allocations. Savings history remains a separate 12-month all-category view with exact monthly values and a plan/recorded trend. Use white cards, section-coloured titles, black body text and readable wrapped continuation rows with repeated headings. Preserve the Bills graph table and calendar styles.

- Overview printing reserves separate name/balance and type/transaction-count lines for every account. Allocate left-column card heights from account and goal counts, preserving padding and the single landscape page without overlapping text.

- Settings Household Tools displays its contents directly without a redundant Tools tab; omit Accounts and Reports tabs. Import opens the existing statement-import subpage. Backup/recovery commands are grouped before import/display/installation commands, using responsive compact rows. Backup lists include a sortable file Date and time column. Tools backup rows match the Bills graph list: white rows, blue selection, sortable plain headings with green sort arrows, fitted columns and vertical scrolling. Preserve backup operations.

- Release checks exercise the actual staged updater subprocess and installed dependencies, supported upgrades, interrupted updates, failure/rollback paths and household-file preservation. Check public feed and package bytes before declaring online availability. Distinguish automated checks from Windows UI, restart and printing verification.

- Settings uses the tab label Tools (formerly Household Tools). Categories retains Budget categories, Income categories and Accounts editing. Help is always the last Settings tab. Test the complete Settings builder and category-list population when changing tab construction.

- Transfer Money uses padded white From/To account cards with existing account-type icons and a direction arrow, compact amount/date controls, five-line Memo and live balances on the selected transfer date. Balance previews exclude the original movement when editing. Stack cards at narrow widths; retain Save/Cancel, Back/Close, validation and Transfer History. Amount entry remains CAD, consistent with the existing ledger.

- Record additions refresh dated lists most recent first while retaining active filters. Entry forms use editable payee/supplier dropdowns and guided CAD category/amount splits; validate positive splits against the expense total. Expenses may retain an optional Due Date, shown in details. Bill payment selects the unpaid supplier/bill and preserves the linked bill, due date and split allocations. Recurring bill duration explicitly selects Number of Payments (including the current bill) or Continuously. Consolidated charts show Date From and Date To below titles, matching each chart’s actual monthly, twelve-month or snapshot coverage.

- Transfer Money guidance is right-aligned beside the left-aligned title. Save, Cancel and Transfer History align with the card edges. Transfer cards, details and memo resize with the window; use compact spacing and retain overflow access at exceptionally small sizes.

- Editable payee/supplier dropdowns use white fields with black text; supplier filters accept typed names. Sort text dropdown choices alphabetically without changing selected/stored values; retain chronological months and numeric sequences. Keep account/category identifiers restricted to existing valid records. Charts date ranges have adjacent calendar icons and filter inclusive dates with From <= To validation; printed charts retain selected ranges. Account charts are balances as of Date To; budget plans include full months touched by the range and state this explicitly. After a new expense, show Transactions and reveal/select the saved record, clearing only filters that hide it. Ordinary expenses remain transactions; do not manufacture duplicate bill entries.

- Add Expense follows Transfer Money with responsive white cards for Expense Details and Amount And Categories, existing account artwork and aligned Save/Cancel. Split category selection fills an empty second or later amount with the unallocated CAD total; preserve typed amounts and validate split totals.

- Expense entry keeps information on the left and Original Image / Split Payment tabs on the right, with a bounded attachment preview. Expense and transfer bottom commands share heights and sit directly below content. Transfer stage guidance uses larger right-aligned text beside Transfer Details. Retain overflow access at small windows and long split lists.

- Back and Close have raised Windows-style 3D button faces; only their surrounding containers match the page/subtitle background. Back uses a large Previous triangle icon. Preserve hover labels, keyboard access and navigation commands.

- Expense and Income entry/detail pages share white cards, large approved artwork and right-hand document/contact tabs; expense splits retain their own tab. Back/Home/Close use round glossy green arrow, blue house and orange-red X controls with matching surrounding backgrounds, hover labels and keyboard access. Home opens Overview; Back goes up one level and Close returns to the section main page.

- Print commands use icon-only 48-pixel artwork matching Back, with hover labels and keyboard access. Budget includes Budget Planner immediately after Manage: monthly expected income, editable CAD category plans, existing historical suggestions, live Left To Plan and a progress bar. Drafts require Save; Reset Draft restores the last saved values. Plans never create recorded income or savings. Print the current draft with explicit labels. Keep the planner category list vertically scrollable without horizontal scrolling.

- Budget Planner Auto Populate Budget reviews the 12 completed months before its month; use recorded split-aware expenses. Variable plans average the months containing recorded spending (all 12 when available); fixed plans use the highest monthly actual in that window. Round Auto Budget estimates up to the nearest $20, keeping exact multiples unchanged; preserve savings goals. For incomplete history, show a friendly best-guess confirmation naming available months and method; no history leaves drafts unchanged. Autofill changes drafts only. Expected Income comes from the selected month’s recorded Income ledger, excluding investment accounts and Interest & dividends/investment income categories; a refresh icon reloads it. Left To Plan, Expenses and Planned Savings are separate white cards with black text. Progress compares total planned expenses plus savings with income; show the excess share in true red. The category list follows the Bills graph white-row, blue-selection style with sortable headings, green arrows, editable plan amounts and vertical scrolling only.

- Update download progress follows actual received bytes and must not round up to 100 percent. Keep completion below 100 until the response closes, expected size and checksum pass, and the package is prepared and compatible. Show verification and preparation explicitly; failures never indicate readiness.

- Budget Planner uses an icon-only Expected Income refresh excluding investments; Total Budget, Total Income and Percentage cards with black text and no explanatory text below. Category icons and Type colour squares compare draft amounts against the highest monthly expense in the previous 12 completed months: green sufficient, red insufficient, grey no comparison or planned savings.

- Planner Expected Monthly Income restores the saved monthly value (including zero); only explicit Refresh replaces the draft with current Income statement records and filters excluding investment accounts/categories. Keep (CAD) on its heading line and use a standalone circular-arrow Refresh icon with no button face or text. Category artwork is stable and distinct; reuse existing semantic artwork and use matching realistic glossy icons for other categories.

- Budget Planner uses one compact toolbar row: Monthly Plan at left, then Expected Monthly Income (CAD), a 40-pixel borderless graphical Refresh, income field and right-aligned Auto Populate Budget. Omit step numbers and the redundant second toolbar row. Preserve refresh keyboard access, hover text and draft saving.

- Budget Planner footer cards appear in order: Total Budget, Total Income, Total Remaining, Percentage. Total Remaining equals expected income minus all planned category amounts, including planned savings, and updates with draft edits. Keep matching white cards, black text, equal widths and no explanatory text below.

- Budget Planner shows sortable Average Actual Spent (CAD) immediately before Your Plan. Use split-aware spending from the previous 12 completed months, averaging months with expense records, without budget rounding. Show a dash for no history and planned savings.

- Planner Refresh uses a standalone circular-arrow icon with no button face; Your Plan amounts have no border. Application message dialogs use white backgrounds, clear graphics and larger text, preserving confirmation/cancellation and keyboard access. Auto Budget alone rounds expense estimates up to the nearest $20 (exact multiples unchanged); preserve fixed/highest versus variable/average history rules and savings goals.

- Refresh and Print use the shared glossy image-only navigation control without rectangular faces. Single-line fields, dropdowns and action controls share a compact 40-pixel height. Preserve transparent icon surroundings, tooltips, keyboard access and borderless planner amounts.

- Auto Populate uses a compact white message with budget-sheet artwork, then a scrollable all-category preview showing Current, Proposed and Up/Down/Unchanged. Cancel preserves the draft and saved plan; Approve And Save immediately saves the reviewed amounts and current Expected Monthly Income atomically. Failed saves preserve both prior draft and saved plan. Popup height follows actual wrapped content; keep long lists scrollable and commands visible. Planner Refresh is 40 pixels; shared single-line fields and action buttons target 40 pixels. Back/Home/Close retain their approved artwork.

- Budget charts share inclusive Date From/Date To controls across Pie, Bar and Trend. Double-click category bars/labels or trend record rows to edit that budget item. Preserve chart artwork; trend records show Source, Actual and Suggested. Calendar launch controls use approved image artwork only with no rectangular face, retaining hover labels and keyboard access. Budget category and actual-record lists show the saved supplier/contact source, falling back to description.

- Suggested budget amounts round historical bases up to a $10 boundary and add $10, preserving zero/no history and overrides. Auto Populate retains its separate $20 rounding. Refresh hover label is Refresh only. Auto Populate review reuses category artwork and shows a red up triangle, green down triangle or yellow unchanged square with spacing before change text. Its explanation has a household-persisted Don’t Show This Again checkbox; never suppress approval review.

- Auto Populate approval headers toggle ascending/descending with numeric amount/change sorting. Budget main-page cards retain approved artwork, enlarged to 112 pixels and top-aligned at the right.

- Auto Populate approval has Total Change for selected rows and a larger instruction card above the list. Rows use checkboxes before larger category artwork, start unselected, and support multiple selection and select all. Save persists only selected category changes; Cancel preserves saved and draft values.

- Calendar launch controls and controls inside calendar views have no hover text. Chart From/To defaults cover the latest year of relevant recorded history, or all available history when shorter, with data matching those dates. Auto Populate approval is a Budget Planner subpage with Back to the retained draft, selectable sortable rows and selected-only Save. Budget category edit screens show the matching large category artwork on the right. Required runtime dependencies belong in the original installer; updates must provide any new requirement or avoid it, and optional graphics add-ons must not block core pages.

- Budget edit forms show Average Actual from the Planner’s previous 12 completed months, using available expense months and split amounts without rounding. Double-click Actual to edit the source payments in that window. Record lists double-click directly into the current record editor; preserve single-click selection, detail commands and the Budget Planner review’s multi-selection. Savings actuals include explicitly classified savings transfers without counting them as expenses. Fictional savings examples add once-only transfers and goal allocations for Emergency Fund A and Retirement Savings; never seed personal households.

- Main-menu section buttons have no vertical gaps. All pie slices and legends use the approved main-menu section palette on screen and in reports; payment statuses retain menu green/red/yellow. Preserve chart shapes, values and separator-free styling.

- Pie charts and matching legends use Brian’s 20-colour reference wheel in clockwise order from the top (red, orange, yellow, green, teal, blue, violet, magenta). Assign by displayed slice order, not category position. Use lighter tints beyond 20 slices. Preserve solid separator-free slices and chart data; this replaces the main-menu palette rule for pies only.

- Budget Trend Graph legends use coloured boxes followed by dark labels on one horizontal line, matching the Bar Chart. Hovering a plotted point shows its month and exact series amounts; overlapping points retain all values.

- Budget pie charts start with main groups (Banking, Utilities, Home and related groups). Single-click a slice or legend to expand its items alongside the other groups; click an expanded item to collapse or another group to switch. Preserve totals, date filters and saved category keys. Update download completion keeps a visible installation review on the same page and reports review-loading errors explicitly.

- Update callbacks must display completion errors and restore retry controls. Coalesce byte progress without dropping verification or result events. Keep Apply Update and Restart above supporting review text. Provide a standalone program repair installer when the installed updater cannot reach review; retain hashes, compatibility, backups, rollback and household preservation.

- Budget pie grouping: Savings belongs to Banking; Health and Leisure belong to Family And Personal; Food and Insurance belong to Home. Indent every expanded subcategory legend row, including its colour swatch, by 24 pixels. Preserve totals and saved category keys.

- Every release must pass the download-to-Ready-To-Install regression gate: real package bytes, size/hash validation, preparation, completion callbacks and visible Apply action, plus truncated/corrupt downloads, network failure, review failure and retry controls. Never mark 100 percent before the review exists. Keep installation controls above release notes. Include trend hover checks after chart repositioning and scrolling when chart code changes.

- Apply Update and standalone repair enumerate only validated numeric PID session files; close-request.json is a command, never an app session. Release checks must reproduce leftover close requests and exercise the actual Apply callback, retaining live-window protection.

- All Budget views share ordered groups Banking (red), Home (yellow), Utilities (green), Transport (light blue), Family And Personal (purple), Giving (pink), Other (peach). Internet belongs to Home; Mobile phone belongs to Family And Personal. Main headings retain position; only individual categories indent and each existing category appears once beneath its parent, including same-named categories. Single-click main pie/bar headings expands or collapses children; individual bar records retain double-click editing. Child colours continue clockwise from the parent in displayed order. Preserve saved keys and totals; no ledger migration.

- Budget Planner and Auto Populate lists use white backgrounds, including category headings and empty areas. Column headings stay fixed above vertically scrolling records and toggle ascending/descending sorting. Preserve grouped categories, draft amounts and Auto Populate selections.

- Update readiness uses additive display: keep Check Again, Download Update and progress in their existing positions; append installation review and Apply Update and Restart below them and above release notes. Never insert review above the download controls.

- Every list heading must align with its data column. Fixed headers and scrolling bodies share identical pixel boundaries, padding and scrollbar allowance; content length must not independently resize either grid. Centre headers over their columns, dates centred and amounts right-aligned. Preserve sorting and selection during resizing.

- Update-page release checks must construct real Tk widgets against the original installed layout helper as well as the current helper. Do not replace dependency construction with mocks in this compatibility check. Avoid passing unsupported layout options to older installed helpers.

- Budget category expansion retains editable borderless From/To fields, calendar actions and the selected shared Pie/Bar/Trend range. Bar subcategory labels indent 24 pixels; bar series use the colours shown in their legend.

- Update and repair completion requires a ready receipt from the reopened app, not only a successful process launch. Test real Windows close, install and restart with a separate disposable household; retain failure logs and retry. Feed checks use a unique request URL to avoid stale cached releases.

- Release numbering starts at v1.2.00 for this repair. Increment the two-digit final component per release: v1.2.01 through v1.2.99, then v1.3.00. Carry every 100 releases into the middle component.

- Standalone repairs are small file-only installers: save a program backup, replace only affected program files, and finish. Do not require Python, consult process/session records, close app windows or reopen the app. This overrides the earlier restart-confirmation requirement for standalone repairs; normal in-app updates retain their restart validation.
