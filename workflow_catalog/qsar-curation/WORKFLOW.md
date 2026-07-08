# QSAR dataset curation

Curate, standardize, and QSAR-ready a raw activity dataset, then hand off to reporting.

Deterministic route: Dataset Curation -> QSAR Report

1. Inspect the raw dataset schema with `qsar_inspect_dataset_schema` and confirm the SMILES / activity / id columns via `qsar_identify_columns`.
2. Curate with `qsar_curate_dataset`: standardize structures, drop invalid rows, deduplicate, and merge activities into a QSAR-ready table.
3. Summarize the curated dataset with `qsar_summarize_curated_dataset` and write the standardization report with `qsar_write_curation_report`.
4. Hand off `clean_dataset_path` and the standardization report to QSAR Report for the final user-facing answer.

Only QSAR Report drafts the final user-facing answer; propagate REPORT_LANGUAGE (English/French) to the final report.
