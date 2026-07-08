# QSAR dataset curation

Standardize, deduplicate, and QSAR-ready a raw activity dataset.

## Procedure

1. Confirm the task is QSAR dataset preparation.
2. Inspect columns with `qsar_inspect_dataset_schema`; map SMILES/activity/id with `qsar_identify_columns`.
3. Curate with `qsar_curate_dataset` (standardize, drop invalid, deduplicate, merge activities).
4. Summarize with `qsar_summarize_curated_dataset` and write the report with `qsar_write_curation_report`.

## Expected Outputs

- clean_dataset_path
- standardization_report_path
