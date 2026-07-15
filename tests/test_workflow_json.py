"""Structural validation for the n8n workflow export.

The workflow JSON is currently a placeholder (empty ``nodes``). These tests
enforce the envelope contract so that when the real export is dropped in, it is
still guaranteed to be a well-formed, importable n8n workflow.
"""

from __future__ import annotations

import json

import jsonschema
import pytest

from conftest import WORKFLOW_PATH


def test_workflow_file_exists() -> None:
    assert WORKFLOW_PATH.is_file(), f"missing workflow export: {WORKFLOW_PATH}"


def test_workflow_is_valid_json() -> None:
    # Fails with a clear message if the export is not parseable JSON.
    json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))


def test_workflow_matches_schema(workflow: dict, workflow_schema: dict) -> None:
    jsonschema.validate(instance=workflow, schema=workflow_schema)


def test_workflow_has_expected_name(workflow: dict) -> None:
    assert workflow["name"] == "Mihar Follow-Up Desk"


def test_workflow_version_is_semver(workflow: dict) -> None:
    version = workflow.get("version", "")
    parts = version.split(".")
    assert len(parts) == 3 and all(
        p.isdigit() for p in parts
    ), f"version must be semver (X.Y.Z), got {version!r}"


def test_nodes_and_connections_are_containers(workflow: dict) -> None:
    assert isinstance(workflow["nodes"], list)
    assert isinstance(workflow["connections"], dict)


def test_node_names_are_unique(workflow: dict) -> None:
    names = [node.get("name") for node in workflow["nodes"]]
    duplicates = {name for name in names if names.count(name) > 1}
    assert not duplicates, f"duplicate node names: {sorted(duplicates)}"


def test_connection_sources_reference_existing_nodes(workflow: dict) -> None:
    node_names = {node.get("name") for node in workflow["nodes"]}
    dangling = [src for src in workflow["connections"] if src not in node_names]
    assert not dangling, f"connections reference unknown nodes: {sorted(dangling)}"


@pytest.mark.skipif(
    True,
    reason="placeholder export has no nodes yet; enable once the real n8n JSON lands",
)
def test_workflow_has_nodes(workflow: dict) -> None:  # pragma: no cover
    assert workflow["nodes"], "real workflow export should define at least one node"
