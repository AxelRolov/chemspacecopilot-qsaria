"""Isolated-QSAR MCP tool specs (curation, training, registry, inference, reporting)."""

from __future__ import annotations

from typing import List

from ..facades.qsar import qsar_facade
from ..tool_adapter import ToolSpec


def _spec(mcp_name: str, method: str, summary: str, *, read_only: bool = False) -> ToolSpec:
    return ToolSpec(
        mcp_name=mcp_name,
        toolkit_factory=qsar_facade,
        method=method,
        summary=summary,
        read_only=read_only,
    )


SPECS: List[ToolSpec] = [
    # Dataset curation
    _spec("qsar_inspect_dataset_schema", "inspect_dataset_schema",
          "Inspect a raw dataset's columns and infer QSAR-relevant fields.", read_only=True),
    _spec("qsar_identify_columns", "identify_columns",
          "Identify SMILES / activity / id columns for QSAR curation.", read_only=True),
    _spec("qsar_curate_dataset", "curate_dataset",
          "Standardize, deduplicate, and merge activities into a QSAR-ready dataset."),
    _spec("qsar_summarize_curated_dataset", "summarize_curated_dataset",
          "Summarize a curated QSAR dataset.", read_only=True),
    _spec("qsar_write_curation_report", "write_curation_report",
          "Write a standardization/curation report artifact."),
    # Training
    _spec("qsar_describe_training_environment", "describe_training_environment",
          "Describe available QSAR training backends and capabilities.", read_only=True),
    _spec("qsar_prepare_training_dataset", "prepare_training_dataset",
          "Prepare and split a curated dataset for a training run."),
    _spec("qsar_train_model", "train_model",
          "Train a QSAR model with the default/auto-selected backend."),
    _spec("qsar_train_chemprop", "train_chemprop",
          "Train a Chemprop message-passing QSAR model."),
    _spec("qsar_train_lightgbm", "train_lightgbm",
          "Train a LightGBM tabular QSAR model."),
    _spec("qsar_train_tabicl", "train_tabicl",
          "Train a TabICL in-context tabular QSAR model."),
    # Model registry / catalog governance
    _spec("qsar_describe_backends", "describe_backends",
          "Describe the registered QSAR prediction backends.", read_only=True),
    _spec("qsar_describe_catalog", "describe_catalog",
          "Describe the QSAR model catalog.", read_only=True),
    _spec("qsar_list_catalog_models", "list_catalog_models",
          "List models available in the QSAR catalog.", read_only=True),
    _spec("qsar_summarize_catalog_model", "summarize_catalog_model",
          "Summarize a specific catalog model.", read_only=True),
    _spec("qsar_recommend_catalog_model", "recommend_catalog_model",
          "Recommend a catalog model for a task/endpoint.", read_only=True),
    _spec("qsar_register_catalog_model", "register_catalog_model",
          "Register a catalog model into the active session registry."),
    _spec("qsar_register_model", "register_model",
          "Register a trained model into the session registry."),
    _spec("qsar_persist_registered_model", "persist_registered_model",
          "Persist a registered model to storage."),
    _spec("qsar_list_registered_models", "list_registered_models",
          "List models registered in the current session.", read_only=True),
    _spec("qsar_summarize_model", "summarize_model",
          "Summarize a registered model.", read_only=True),
    # Inference
    _spec("qsar_predict_from_csv", "predict_from_csv",
          "Run predictions for a CSV of structures with a registered model."),
    _spec("qsar_predict_from_smiles", "predict_from_smiles",
          "Run predictions for SMILES with a registered model."),
    _spec("qsar_export_prediction_summary", "export_prediction_summary",
          "Export a summary of the latest prediction run."),
    # Reporting
    _spec("qsar_init_report_payload", "init_report_payload",
          "Initialize a structured QSAR report payload."),
    _spec("qsar_append_report_section", "append_report_section",
          "Append a section to the QSAR report payload."),
    _spec("qsar_build_prediction_report_payload", "build_prediction_report_payload",
          "Build a report payload from the latest prediction state."),
    _spec("qsar_export_latex_report", "export_latex_report",
          "Export the QSAR report payload to a LaTeX artifact."),
    _spec("qsar_export_latest_prediction_bundle", "export_latest_prediction_bundle",
          "Export the latest prediction report bundle."),
]
