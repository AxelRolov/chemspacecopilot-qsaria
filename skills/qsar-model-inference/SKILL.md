# QSAR model inference

Run predictions with a registered model and report values with applicability domain.

## Procedure

1. Resolve the model (registered or recommended/registered from the catalog).
2. Predict with `qsar_predict_from_smiles` or `qsar_predict_from_csv`; capture applicability-domain flags.
3. Summarize with `qsar_export_prediction_summary`.

## Expected Outputs

- latest_predictions_csv
- prediction_summary
