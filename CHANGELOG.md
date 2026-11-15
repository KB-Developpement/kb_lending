# Changelog

All notable changes to KB Lending are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
`.github/workflows/release.yml` reads the section matching a pushed `v*.*.*` tag
and uses it as the GitHub Release body, so every released version needs a
`## [x.y.z]` heading here.

## [Unreleased]

## [1.0.2] — 2026-11-15

### Changed

- French names for the roles « Loan Officer » (« Chargé de prêts »), « Loan Processor » (« Chargé du traitement des prêts »), « Loan Appraiser » (« Évaluateur de prêts ») and « Loan Underwriter » (« Analyste crédit »).

## [1.0.1] — 2026-11-14

### Fixed

- French translations aligned with the platform wording (frappe, kb_pro) for labels the platform
  already translates, since an app's translation overrides it across the whole desk (« Liaisons »,
  « Validé », « Mode de règlement », « Reste à payer », « Réglé » instead of « Colonisé »…);
  « Montants » and « N° de référence » in `translations/fr.csv`. No entry is added or removed.

## [1.0.0] — 2026-11-04

First KB Développement release of the lending app, forked from Frappe Lending.

### Changed

- **Runs on KB Pro instead of ERPNext**: `required_apps` is `frappe/kb_pro`, and every
  `erpnext.*` import and call (general ledger, accounts controller, journal entry, default
  company, currency and cost center, test helpers) now goes through `kb_pro`.
- **App renamed from `lending` to `kb_lending`**: the folder, the Python package
  (`kb_lending`), `app_name`, the distribution name, every `lending.*` dotted path (imports,
  hooks, scheduler events, `patches.txt`, `frappe.call` methods) and the `/assets/lending/`
  paths now use `kb_lending`. Kept on purpose: the `/app/lending` workspace route, the
  `lending.common` JavaScript namespace and the `lending.bundle.js` bundle name.

### Upgrading an existing site

Renaming an installed app is not handled by `bench migrate`. On a site that has `lending`
installed, together with this release:

1. Move `apps/lending` to `apps/kb_lending`, replace `lending` with `kb_lending` in
   `sites/apps.txt` and `sites/apps.json`, then `pip uninstall lending` and
   `pip install -e apps/kb_lending`.
2. In the site database, set `app` / `app_name` from `lending` to `kb_lending` (Installed
   Application, Module Def, …), prefix `tabPatch Log` and `tabScheduled Job Type` entries
   `lending.*` with `kb_lending.*`, and replace `"lending"` in the `installed_apps` default.
3. Flush the Redis cache, run `bench migrate`, `bench build --app kb_lending`, and restart the
   bench.

Requires KB Pro 1.4.1 or later, and KB RH 1.0.3 or later when HR is installed.

---
