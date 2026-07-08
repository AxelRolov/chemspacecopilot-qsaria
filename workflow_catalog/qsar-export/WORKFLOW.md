# QSAR report export

Export the latest QSAR prediction/training state to a LaTeX report or payload bundle.

Deterministic route: QSAR Report

1. Treat a standalone `latex` / `@latex` token or an export request for the latest prediction as a documentation export.
2. Do not rerun prediction; export the latest completed prediction/training state.
3. Build the payload with `qsar_build_prediction_report_payload` if needed, then export with `qsar_export_latex_report` / `qsar_export_latest_prediction_bundle`.
4. Return the QSAR Report answer verbatim.

Only QSAR Report drafts the final user-facing answer; propagate REPORT_LANGUAGE (English/French) to the final report.
