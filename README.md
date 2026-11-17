# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
"# CryoSyncFront"

## Background job intervals

Both background jobs run once per day by default. To change them:

| Job | Setting | Where to change |
| --- | --- | --- |
| AI temperature-incident scan | `AI_SCAN_INTERVAL_MINUTES` (default `1440`) | `app.yaml` (Databricks Apps) or `backend/.env` / `backend/.env.example` (local). Code default: `backend/main.py` → `_scan_interval_seconds()`. |
| Zoho CRM → Databricks sync | `ZOHO_SYNC_INTERVAL_MINUTES` (default `1440`) | `app.yaml` (Databricks Apps) or `backend/.env` / `backend/.env.example` (local). Code default: `backend/main.py` → `_zoho_sync_interval_seconds()`. |

Values are in minutes; `0` disables a background loop. Restart the app after changing an interval (values are read once at startup).

Zoho CRM can also be synced on demand from **Admin → Sync Zoho CRM** (calls `POST /api/admin/sync-zoho`). It requires `CRYOSYNC_DB_BACKEND=databricks` plus the Zoho credentials.
