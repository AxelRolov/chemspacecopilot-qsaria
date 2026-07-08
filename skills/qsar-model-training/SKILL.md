# QSAR model training

Train and validate a QSAR model on a curated dataset using a chosen backend.

## Procedure

1. Require a curated QSAR-ready dataset; run the curation skill first if the input is raw.
2. Inspect capabilities with `qsar_describe_training_environment`.
3. Prepare and split with `qsar_prepare_training_dataset`.
4. Train with `qsar_train_model` or a specific backend (`qsar_train_chemprop`/`qsar_train_lightgbm`/`qsar_train_tabicl`).

## Expected Outputs

- trained_model_path
- training_metrics
