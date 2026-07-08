"""Isolated-QSAR facade for MCP tool registration.

Exposes the fork's QSAR sub-system (curation, training, model registry,
inference, reporting) to external MCP clients. A single shared prediction
backend registry is built once so the registry, inference, and reporting
toolkits operate on a consistent catalog. Cross-call state (registered models,
latest prediction) flows through the per-call ``agent`` context injected by the
tool adapter, mirroring how the Agno QSAR team shares ``session_state``.
"""

from __future__ import annotations

import functools


class QSARFacade:
    """Adapter exposing the isolated QSAR toolkits as flat MCP methods."""

    def __init__(self) -> None:
        from cs_copilot.tools import (
            DatasetCurationToolkit,
            ModelRegistryToolkit,
            PredictionInferenceToolkit,
            QSARReportingToolkit,
            QSARTrainingToolkit,
            build_default_prediction_backends,
        )

        backends = build_default_prediction_backends()
        registry = ModelRegistryToolkit(backends=backends)
        inference = PredictionInferenceToolkit(backends=backends, registry_toolkit=registry)
        curation = DatasetCurationToolkit()
        training = QSARTrainingToolkit()
        reporting = QSARReportingToolkit()

        # Dataset curation
        self.inspect_dataset_schema = curation.inspect_dataset_schema
        self.identify_columns = curation.identify_qsar_columns
        self.curate_dataset = curation.curate_qsar_dataset
        self.summarize_curated_dataset = curation.summarize_curated_dataset
        self.write_curation_report = curation.write_curation_report

        # Training
        self.describe_training_environment = training.describe_qsar_training_environment
        self.prepare_training_dataset = training.prepare_training_dataset
        self.train_model = training.train_qsar_model
        self.train_chemprop = training.train_chemprop_model
        self.train_lightgbm = training.train_lightgbm_model
        self.train_tabicl = training.train_tabicl_model

        # Model registry / catalog governance
        self.describe_backends = registry.describe_backends
        self.describe_catalog = registry.describe_catalog
        self.list_catalog_models = registry.list_catalog_models
        self.summarize_catalog_model = registry.summarize_catalog_model
        self.recommend_catalog_model = registry.recommend_catalog_model
        self.register_catalog_model = registry.register_catalog_model
        self.register_model = registry.register_model
        self.persist_registered_model = registry.persist_registered_model
        self.list_registered_models = registry.list_registered_models
        self.summarize_model = registry.summarize_model

        # Inference
        self.predict_from_csv = inference.predict_from_csv
        self.predict_from_smiles = inference.predict_from_smiles
        self.export_prediction_summary = inference.export_prediction_summary

        # Reporting
        self.init_report_payload = reporting.init_qsar_report_payload
        self.append_report_section = reporting.append_qsar_report_section
        self.build_prediction_report_payload = reporting.build_prediction_report_payload
        self.export_latex_report = reporting.export_qsar_latex_report
        self.export_latest_prediction_bundle = reporting.export_latest_prediction_report_bundle


@functools.lru_cache(maxsize=1)
def qsar_facade() -> QSARFacade:
    return QSARFacade()
