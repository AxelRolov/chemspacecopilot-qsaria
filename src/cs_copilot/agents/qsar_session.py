#!/usr/bin/env python
# coding: utf-8
"""Shared session-state scaffolding for the isolated QSAR agents.

This is intentionally free of routing logic — route selection lives in
``qsar_flow`` (the Agno ``Workflow`` router) and is documented by the
``workflow_catalog/qsar-*`` contracts. These helpers only build the mutable
``session_state`` skeleton the QSAR agents share.
"""

from __future__ import annotations

import copy
from typing import Any, Dict


def default_prediction_state() -> Dict[str, Any]:
    return {
        "registered": {},
        "last_prediction": {},
        "prediction_history": [],
        "catalog_recommendations": {},
        "training_runs": [],
        "active_training_run": None,
    }


def default_qsar_session_state() -> Dict[str, Any]:
    """Return the shared QSAR state skeleton used by all isolated QSAR agents."""
    return {
        "prediction_models": default_prediction_state(),
        "prediction_outputs": {
            "latest_predictions_csv": None,
            "latest_summary": None,
        },
        "qsar_curation": {
            "last_request": {},
            "last_result": {},
            "history": [],
        },
        "qsar_training": {
            "last_request": {},
            "last_result": {},
        },
        "qsar_registry": {
            "last_request": {},
            "last_result": {},
        },
        "qsar_inference": {
            "last_request": {},
            "last_result": {},
        },
        "qsar_report": {
            "last_request": {},
            "last_result": {},
        },
        "qsar_workflow": {
            "last_plan": {},
            "history": [],
        },
    }


def copy_qsar_session_state() -> Dict[str, Any]:
    """Return an independent copy of the default QSAR state."""
    return copy.deepcopy(default_qsar_session_state())
