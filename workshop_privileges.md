# Trade Me Data Seekers Workshop — Required Privileges

This document outlines all Snowflake privileges and account-level settings required for participants to complete the workshop.

---

## 1. Account-Level Settings (ACCOUNTADMIN)

These settings must be configured before the workshop begins.

| Setting | Value | Reason |
|---------|-------|--------|
| `CORTEX_ENABLED_CROSS_REGION` | `ANY_REGION` (recommended) or `AWS_US` | CoCo requires access to Claude models which are not hosted in AP-Southeast (Sydney). Cross-region inference routes requests to regions where models are available. |
| Web Search | Enabled via Snowsight UI: **AI/ML > Agents > Settings > Web search toggle** | Enables CoCo to search the web as part of answering questions or completing tasks (Cloud Agents feature). |

---

## 2. Compute Pool Access (for Streamlit in Workspaces)

Streamlit apps in Workspaces run on SPCS (Snowpark Container Services). Users need access to a compute pool.

| Requirement | Detail |
|-------------|--------|
| Compute pool exists | A compute pool must be created with `INSTANCE_FAMILY = CPU_X64_XS` (or similar) and `AUTO_RESUME = TRUE` |
| `USAGE` privilege on the compute pool | The user's role must have USAGE on the compute pool |
| `ALLOWED_SPCS_WORKLOAD_TYPES` includes `STREAMLIT` | Default is `ALL` which includes STREAMLIT, but admins may have restricted this |

---

## 3. Database, Schema & Table Access

| Privilege | Object | Modules |
|-----------|--------|---------|
| `USAGE` | Database `TM_WORKSHOP` | All |
| `USAGE` | Schema `TM_WORKSHOP.SAMPLEDATA` | All |
| `SELECT` | `TM_WORKSHOP.SAMPLEDATA.JOBS_LISTINGS` | 1, 2 |
| `SELECT` | `TM_WORKSHOP.SAMPLEDATA.MOTORS_LISTINGS` | 2 |
| `SELECT` | `TM_WORKSHOP.SAMPLEDATA.MARKETPLACE_LISTINGS` | 3, 4 |
| `SELECT` | `TM_WORKSHOP.SAMPLEDATA.AD_REVENUE` | 4 |
| `SELECT` | `TM_WORKSHOP.SAMPLEDATA.CONTACTS` | 3, 4 |

A blanket `SELECT ON ALL TABLES IN SCHEMA` is recommended in case CoCo discovers additional tables during exploration.

---

## 4. Warehouse Access

| Privilege | Object | Reason |
|-----------|--------|--------|
| `USAGE` | A virtual warehouse | Running all SQL queries and Streamlit app compute |

---

## 5. Workspace Access

| Requirement | Detail |
|-------------|--------|
| Workspace creation | Typically available to all users via their personal `USER$` schema — no explicit grant needed unless the account has restricted this |

---

## 6. CoCo (Cortex Code) Access

### Database Roles Required

| Database Role | Reason |
|---------------|--------|
| `SNOWFLAKE.COPILOT_USER` | Required for all users to access CoCo in Snowsight |
| `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_AGENT_USER` | At least one is required. `CORTEX_USER` is granted to `PUBLIC` by default but may have been revoked. |

### Model Access

| Requirement | Detail |
|-------------|--------|
| Cross-region inference enabled | Required because Claude models are not available locally in AP-Southeast (Sydney) |
| `CORTEX_MODELS_ALLOWLIST` | If configured, must include the models CoCo uses (e.g., `claude-opus-4-6`, `claude-sonnet-4-6`) |

### Cloud Agents (Shell, Python, Web Search)

| Feature | Requirement |
|---------|-------------|
| Cloud Agents (shell/Python execution) | Generally available in all commercial regions — no additional config needed |
| Web Search | Must be explicitly enabled by ACCOUNTADMIN via Snowsight: **AI/ML > Agents > Settings > Web search toggle** |
| Non-Snowflake egress (package installs) | Allowed by default. Can be blocked by setting `COCO_CLOUD_AGENTS_NON_SNOWFLAKE_EGRESS_DISABLED = TRUE` — ensure this is **not** set to TRUE |

---

## 7. Streamlit Deployment

| Privilege | Object | Reason |
|-----------|--------|--------|
| `CREATE STREAMLIT` | On the target schema (if deploying outside workspace) | Module 4 — only needed if deploying as a standalone Streamlit object |
| `USAGE` on compute pool | Compute pool with STREAMLIT workload allowed | Required to run Streamlit apps within Workspaces |

---

## Summary Checklist

- [ ] `CORTEX_ENABLED_CROSS_REGION` set to `ANY_REGION` or `AWS_US`
- [ ] Web search enabled in **AI/ML > Agents > Settings**
- [ ] Compute pool created and accessible to workshop role
- [ ] `USAGE` granted on `TM_WORKSHOP` database and `SAMPLEDATA` schema
- [ ] `SELECT` granted on all tables in `TM_WORKSHOP.SAMPLEDATA`
- [ ] `USAGE` granted on a warehouse
- [ ] `SNOWFLAKE.COPILOT_USER` database role available to workshop users
- [ ] `SNOWFLAKE.CORTEX_USER` database role available to workshop users
- [ ] `COCO_CLOUD_AGENTS_NON_SNOWFLAKE_EGRESS_DISABLED` is NOT set to TRUE
- [ ] `CORTEX_MODELS_ALLOWLIST` (if set) includes Claude models

---

## Notes

- **CoCo in Snowsight** always starts a session using the user's **default role**, regardless of the role selected in the Snowsight role selector. Ensure the user's default role has all the privileges above.
- **Cross-region inference** is the most commonly missed prerequisite for Sydney-based accounts. Without it, CoCo will fail with model availability errors.
- **AWS_APJ** cross-region setting may be limited to Claude Sonnet 4.0 only — use `AWS_US` or `ANY_REGION` for full model access including Opus models.
- **Skills** (Module 3c) are stored in the user's personal workspace under `.snowflake/cortex/skills/` — no additional write privileges to shared schemas are needed.
