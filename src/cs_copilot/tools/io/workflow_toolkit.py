"""Agno toolkit for consulting ChemSpace reusable workflow contracts."""

from __future__ import annotations

from typing import Any, Dict, List

from agno.tools.toolkit import Toolkit

from cs_copilot.workflows import get_workflow, list_workflows, search_workflows


class WorkflowToolkit(Toolkit):
    """Read-only access to the ChemSpace workflow catalog."""

    def __init__(self) -> None:
        super().__init__("workflows")
        self.register(self.list_workflows)
        self.register(self.search_workflows)
        self.register(self.fetch_workflow)

    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all reusable ChemSpace multi-step workflow contracts."""

        return [workflow.as_dict(include_content=False) for workflow in list_workflows()]

    def search_workflows(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search ChemSpace workflows by topic, tool, artifact, or workflow name."""

        return [
            workflow.as_dict(include_content=False)
            for workflow in search_workflows(query, limit=max(1, int(limit)))
        ]

    def fetch_workflow(self, slug: str) -> Dict[str, Any]:
        """Fetch one ChemSpace workflow, including its full WORKFLOW.md content."""

        return get_workflow(slug).as_dict(include_content=True)
