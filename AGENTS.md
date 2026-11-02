# NestSimple Money

- GitHub repository: Shavastar/NestSimple-Money-Updates. Releases are published through its versioned packages and latest.json feed.
- Release numbering starts at v1.2.00 for the repair following v1.0.199. Increment the two-digit final component: v1.2.01 through v1.2.99, then v1.3.00. Every 100 releases carries into the middle component.
- Before publishing, test the actual packaged executable on Windows using a disposable installation and a separate fictional household. Verify closing multiple app windows, package validation, backup, installation, reopening, version, and the same household. A successful process launch alone is not successful restart.
- Exercise startup failure and retry, failed/corrupt/truncated downloads, feed freshness, review visibility, rollback and household preservation. Keep diagnostic details available when anything fails. Never claim an unperformed check passed.
- Preserve personal and testing household data and edits. Repair program files only. Do not replace household databases or profile files.
- Keep the shared STYLE_GUIDE.md and release history current.

- Standalone repairs must be small native file-only installers: back up affected program files and replace them directly. No Python requirement, session checks, process shutdown or app reopening. This supersedes restart requirements above for standalone repairs only.

- Do not open test app windows, test dialogs or installers on the user desktop unless the user explicitly requests it. Prefer background and headless verification, and state when visual or full GUI checks were not performed.

- All in-app message boxes are page-owned bottom sheets with slide-up/down transitions, large shared illustrations and status icons. Preserve answer values and Enter/Escape behavior; do not restore separate message Toplevel windows. Auto Populate Review shows Planner average Actuals in CAD, with numeric signed-change sorting and fixed category-group order.
