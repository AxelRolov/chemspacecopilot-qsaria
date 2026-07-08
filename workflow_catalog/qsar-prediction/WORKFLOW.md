# QSAR prediction / inference

Run predictions with a registered/selected model and report results and applicability domain.

Deterministic route: Model Inference -> QSAR Report

1. Resolve the model to use: an already-registered model, or recommend/register one from the catalog with `qsar_recommend_catalog_model` / `qsar_register_catalog_model`.
2. Predict with `qsar_predict_from_smiles` for inline structures or `qsar_predict_from_csv` for a dataset; capture applicability-domain flags.
3. Summarize with `qsar_export_prediction_summary` and build the report payload with `qsar_build_prediction_report_payload`.
4. Hand the predictions and summary to QSAR Report.

Only QSAR Report drafts the final user-facing answer; propagate REPORT_LANGUAGE (English/French) to the final report.
