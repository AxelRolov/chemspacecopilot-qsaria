#!/usr/bin/env python
# coding: utf-8
"""Deterministic QSAR routing, realized as a native Agno ``Workflow``.

This replaces the old regex-classifier module (``qsar_workflow.py``). Route
*definitions* live in the ``workflow_catalog/qsar-*`` contracts (their
``keywords:`` mirror the triggers below); this module owns the executable
selector and compiles the routes into an Agno ``Workflow`` whose first step is a
``Router`` that dispatches to a fixed ``Steps`` sequence of QSAR agents. The
selector is deterministic (no LLM), preserving the guarantee the old classifier
provided.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from agno.models.base import Model
from agno.workflow import Router, Step, Steps, Workflow

from .qsar_session import copy_qsar_session_state


class QSARWorkflowKind(str, Enum):
    """Known deterministic QSAR routes."""

    CURATION_ONLY = "curation_only"
    TRAINING = "training"
    PREDICTION = "prediction"
    REGISTRY = "registry"
    ENSEMBLE = "ensemble"
    EXPORT_ONLY = "export_only"


QSAR_AGENT_ROUTES: Dict[QSARWorkflowKind, Tuple[str, ...]] = {
    QSARWorkflowKind.CURATION_ONLY: ("dataset_curation", "qsar_report"),
    QSARWorkflowKind.TRAINING: (
        "dataset_curation",
        "qsar_training",
        "model_registry",
        "qsar_report",
    ),
    QSARWorkflowKind.PREDICTION: ("model_inference", "qsar_report"),
    QSARWorkflowKind.REGISTRY: ("model_registry", "qsar_report"),
    QSARWorkflowKind.ENSEMBLE: ("model_registry", "qsar_report"),
    QSARWorkflowKind.EXPORT_ONLY: ("qsar_report",),
}

# Route -> workflow_catalog slug (the declarative contract for each route).
QSAR_KIND_TO_SLUG: Dict[QSARWorkflowKind, str] = {
    QSARWorkflowKind.CURATION_ONLY: "qsar-curation",
    QSARWorkflowKind.TRAINING: "qsar-training",
    QSARWorkflowKind.PREDICTION: "qsar-prediction",
    QSARWorkflowKind.REGISTRY: "qsar-registry",
    QSARWorkflowKind.ENSEMBLE: "qsar-ensemble",
    QSARWorkflowKind.EXPORT_ONLY: "qsar-export",
}

QSAR_AGENT_NAMES: Dict[str, str] = {
    "dataset_curation": "Dataset Curation",
    "qsar_training": "QSAR Training",
    "model_registry": "Model Registry",
    "model_inference": "Model Inference",
    "qsar_report": "QSAR Report",
}

_LATEX_SHORTCUT_RE = re.compile(r"^\s*@?latex\s*$", re.I)
_FRENCH_SIGNAL_RE = re.compile(
    r"\b(cr[eé]e|créer|entraine|entra[iî]ne|pr[eé]dis|pr[eé]dire|mod[eè]le|"
    r"jeu de donn[eé]es|r[eé]sume|rapport|fichier|g[eé]n[eè]re|g[eé]n[eé]rer)\b",
    re.I,
)
_EXPORT_RE = re.compile(r"\b(latex|payload|tex|export|exporte|g[eé]n[eè]re|g[eé]n[eé]rer)\b", re.I)
_PREDICTION_CONTEXT_RE = re.compile(
    r"\b(latest|derni[eè]re|prediction|pr[eé]diction|payload)\b", re.I
)
_ENSEMBLE_RE = re.compile(r"\b(ensemble|consensus)\b", re.I)
_ENSEMBLE_ACTION_RE = re.compile(
    r"\b(create|build|make|summari[sz]e|list|inspect|compare|cr[eé]e|créer|r[eé]sume)\b",
    re.I,
)
_TRAINING_RE = re.compile(
    r"\b(train|training|fit|validate|validation|benchmark|chemprop|lightgbm|tabicl|"
    r"entrain|entra[iî]n|apprendre)\b",
    re.I,
)
_CURATION_RE = re.compile(
    r"\b(curate|curation|clean|prepare|standardi[sz]e|deduplicate|dataset schema|"
    r"pr[eé]pare|nettoie|jeu de donn[eé]es)\b",
    re.I,
)
_PREDICTION_RE = re.compile(
    r"\b(predict|prediction|infer|inference|screen|applicability domain|ad |"
    r"lipophilicity|pr[eé]dis|pr[eé]diction|inf[eé]rence)\b",
    re.I,
)
_REGISTRY_RE = re.compile(
    r"\b(catalog|catalogue|registry|register|model summary|model comparison|recommend|"
    r"backend|capability|capabilities|available models|mod[eè]les disponibles|"
    r"backends?)\b",
    re.I,
)


@dataclass(frozen=True)
class QSARWorkflowPlan:
    """A deterministic routing decision for the QSAR sub-system."""

    workflow: QSARWorkflowKind
    route: Tuple[str, ...]
    report_language: str
    export_only: bool = False
    rerun_prediction: bool = True

    @property
    def slug(self) -> str:
        return QSAR_KIND_TO_SLUG[self.workflow]

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["workflow"] = self.workflow.value
        payload["route"] = list(self.route)
        payload["slug"] = self.slug
        return payload


def detect_report_language(message: str) -> str:
    """Return the report language required by the latest user message."""
    text = message or ""
    return "French" if _FRENCH_SIGNAL_RE.search(text) else "English"


def classify_qsar_workflow(message: str) -> QSARWorkflowPlan:
    """Classify a user request into the supported QSAR workflow routes.

    Ordered, conservative, and deterministic — the same high-level routes the
    ``workflow_catalog/qsar-*`` contracts describe.
    """
    text = message or ""
    language = detect_report_language(text)

    if _LATEX_SHORTCUT_RE.match(text) or (
        _EXPORT_RE.search(text) and _PREDICTION_CONTEXT_RE.search(text)
    ):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.EXPORT_ONLY,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.EXPORT_ONLY],
            report_language=language,
            export_only=True,
            rerun_prediction=False,
        )

    if _ENSEMBLE_RE.search(text) and _ENSEMBLE_ACTION_RE.search(text):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.ENSEMBLE,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.ENSEMBLE],
            report_language=language,
        )

    if _TRAINING_RE.search(text):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.TRAINING,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.TRAINING],
            report_language=language,
        )

    if _PREDICTION_RE.search(text):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.PREDICTION,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.PREDICTION],
            report_language=language,
        )

    if _REGISTRY_RE.search(text):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.REGISTRY,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.REGISTRY],
            report_language=language,
        )

    if _CURATION_RE.search(text):
        return QSARWorkflowPlan(
            workflow=QSARWorkflowKind.CURATION_ONLY,
            route=QSAR_AGENT_ROUTES[QSARWorkflowKind.CURATION_ONLY],
            report_language=language,
        )

    return QSARWorkflowPlan(
        workflow=QSARWorkflowKind.REGISTRY,
        route=QSAR_AGENT_ROUTES[QSARWorkflowKind.REGISTRY],
        report_language=language,
    )


def plan_qsar_workflow(message: str) -> Dict[str, Any]:
    """Return the deterministic QSAR route for a user message as plain data."""
    return classify_qsar_workflow(message).to_dict()


def describe_qsar_routes() -> str:
    """Return a compact, prompt-safe description of deterministic QSAR routes."""
    lines = []
    for workflow, route in QSAR_AGENT_ROUTES.items():
        readable_route = " -> ".join(QSAR_AGENT_NAMES[item] for item in route)
        lines.append(f"- {QSAR_KIND_TO_SLUG[workflow]}: {readable_route}")
    return "\n".join(lines)


def build_qsar_workflow(
    model: Model,
    *,
    markdown: bool = True,
    debug_mode: bool = False,
    enable_mlflow_tracking: bool = True,
    session_id: Optional[str] = None,
    db: Any = None,
) -> Workflow:
    """Compile the deterministic QSAR routes into a native Agno ``Workflow``.

    The workflow's single step is a ``Router`` whose selector classifies the
    request (deterministically, via :func:`classify_qsar_workflow`) and returns
    the matching route as a ``Steps`` sequence of QSAR agents. ``qsar_report`` is
    always the terminal step, so it drafts the final user-facing answer.
    """
    # Imported here to avoid a circular import at module load (factories imports
    # qsar_session; registry imports factories).
    from .factories import QSARServiceContext
    from .registry import create_agent

    qsar_context = QSARServiceContext.create()
    agent_params = {
        "markdown": markdown,
        "debug_mode": debug_mode,
        "enable_mlflow_tracking": enable_mlflow_tracking,
        "qsar_context": qsar_context,
    }
    agents = {
        agent_type: create_agent(agent_type, model=model, **agent_params)
        for agent_type in QSAR_AGENT_NAMES
    }

    route_choices = []
    routes_by_kind: Dict[QSARWorkflowKind, Steps] = {}
    for kind, route in QSAR_AGENT_ROUTES.items():
        slug = QSAR_KIND_TO_SLUG[kind]
        # Fresh Step wrappers per route (agents are shared) so choices never
        # collide on step identity.
        steps = [
            Step(name=f"{slug}:{QSAR_AGENT_NAMES[a]}", agent=agents[a]) for a in route
        ]
        sequence = Steps(name=slug, steps=steps)
        routes_by_kind[kind] = sequence
        route_choices.append(sequence)

    def _select_route(step_input):
        text = step_input.get_input_as_string() or ""
        plan = classify_qsar_workflow(text)
        return routes_by_kind[plan.workflow]

    router = Router(
        name="qsar-router",
        description="Deterministically route a QSAR request to its fixed agent sequence.",
        selector=_select_route,
        choices=route_choices,
    )

    return Workflow(
        name="QSAR Workflow",
        description="Isolated QSAR sub-system: deterministic curation/training/"
        "prediction/registry/ensemble/export routes.",
        steps=[router],
        session_state=copy_qsar_session_state(),
        session_id=session_id,
        db=db,
    )
