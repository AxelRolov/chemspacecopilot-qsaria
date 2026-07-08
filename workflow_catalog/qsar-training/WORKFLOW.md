# QSAR model training

Curate (if needed), train and validate a QSAR model, register it, and report metrics.

Deterministic route: Dataset Curation -> QSAR Training -> Model Registry -> QSAR Report

1. Ensure a curated, QSAR-ready dataset exists; run the `qsar-curation` workflow first when the input is raw.
2. Prepare and split the training data with `qsar_prepare_training_dataset`.
3. Train with `qsar_train_model` (auto-select backend) or a specific backend: `qsar_train_chemprop`, `qsar_train_lightgbm`, or `qsar_train_tabicl`.
4. Register the trained model with `qsar_register_model` and persist it with `qsar_persist_registered_model` when the user wants it kept.
5. Hand training metrics and the registered model to QSAR Report.

Only QSAR Report drafts the final user-facing answer; propagate REPORT_LANGUAGE (English/French) to the final report.
