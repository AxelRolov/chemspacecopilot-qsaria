# QSAR reporting

Draft the final QSAR answer and export LaTeX/payload bundles in the required language.

## Procedure

1. QSAR Report is the only agent that drafts the final user-facing answer.
2. Build the payload with `qsar_init_report_payload` / `qsar_build_prediction_report_payload`.
3. Export with `qsar_export_latex_report` / `qsar_export_latest_prediction_bundle`.
4. Honor REPORT_LANGUAGE (English/French) even when tool outputs are in another language.

## Expected Outputs

- qsar_latex_path
- report_bundle
