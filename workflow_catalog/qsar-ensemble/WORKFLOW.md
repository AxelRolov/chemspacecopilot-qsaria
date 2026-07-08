# QSAR ensemble

Create or summarize a consensus ensemble over compatible catalog models, then report.

Deterministic route: Model Registry -> QSAR Report

1. Interpret `ensemble QSAR` / `consensus QSAR` as an ensemble of predictive models, not a dataset.
2. Inspect compatible catalog models with `qsar_list_catalog_models`; select components via `qsar_recommend_catalog_model`.
3. Create/summarize the ensemble; state that evaluation needs a separate explicit dataset request.
4. Hand the ensemble summary to QSAR Report.

Only QSAR Report drafts the final user-facing answer; propagate REPORT_LANGUAGE (English/French) to the final report.
