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

## Long-Term Vision and Modular Engine Roadmap

While the immediate focus of this cleanup plan is to stabilize and get Seismograph reliably logging data, it's important to keep in mind our long-term architectural goals and business vision. This section outlines the direction we intend to evolve towards once the current cleanup is complete.

### Modular Engine Architecture

- **Refactor loggers into modular "engines":**  
  Each metric or data source should become an isolated, reusable engine module with a consistent interface (e.g., a class with a `run()` method).  
- **Centralized orchestrator:**  
  Develop an orchestrator to manage execution flow, scheduling, retries, and error handling across all engines.  
- **Extensible and maintainable codebase:**  
  This approach facilitates adding new metrics, upgrading existing ones, and maintaining clean separation of concerns.  
- **Scalable project structure:**  
  Engines can be independently tested, updated, and even monetized as standalone components.

### Business and Monetization Potential

- **SaaS Platform:**  
  Build a web-based UI/dashboard presenting real-time and historical analytics, configurable alerts, and performance insights powered by Seismograph’s data.  
- **Integration with Communication Platforms:**  
  Utilize Discord, Telegram, or other chat platforms to push notifications, signals, and reports to users in real-time.  
- **Subscription Model:**  
  Offer tiered access to data streams, analysis tools, and premium signals.  
- **Consulting and Custom Solutions:**  
  Provide tailored data insights and system integrations for institutional clients or active traders.  
- **Open-Source Core + Paid Add-ons:**  
  Maintain the core engine as open source to build community trust and contributions, while developing proprietary add-ons for monetization.

---

This vision will guide our architectural decisions moving forward and ensure Seismograph not only meets our current needs but also becomes a robust foundation for future growth and opportunity.
