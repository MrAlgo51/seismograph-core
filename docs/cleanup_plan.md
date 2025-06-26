# Seismograph Database Cleanup & Returns Upgrade Plan

## 1. Audit & Clean Redundant Z-Score Columns

- Identify redundant z-score columns:
  - `premium_zscore` vs `premium_z`
  - `spread_zscore` vs `spread_z`
- Check logger/analysis code to find used columns.
- Pick a canonical z-score column for each metric.
- Migrate data if needed, then drop duplicates.
- Update code to use canonical columns only.

## 2. Standardize Timestamp Format

- Use **INTEGER UNIX timestamps** consistently across all tables.
- Migrate tables with `TEXT` timestamps to INTEGER.
- Update all code and queries accordingly.

## 3. Remove Legacy Columns

- Identify obsolete columns like `score` in `signals`.
- Remove columns after verifying no code dependency.
- Clean up references in the codebase.

## 4. Review & Refactor Logger Scripts

- Ensure loggers write to updated schema.
- Confirm use of canonical z-score columns.
- Confirm use of standardized timestamps.
- Add any new fields as needed.

## 5. Design & Implement New Returns Table

- Support multi-horizon returns aligned with 5-score system.
- Use standardized timestamps.
- Build new logger to populate the returns table.

## 6. Testing & Validation

- Run loggers, verify data accuracy.
- Check query correctness.
- Validate z-score and score calculations.
- Test end-to-end data flow.

## 7. Documentation & Maintenance

- Document schema changes and logger behaviors.
- Maintain migration and version control notes.
- Keep documentation updated for future devs.

---

> **Note:** Starting clean is essential for a reliable, maintainable system. This plan lays the groundwork for scaling and improving Seismograph.

