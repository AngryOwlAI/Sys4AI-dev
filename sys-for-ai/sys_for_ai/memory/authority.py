"""Authority classification for memory objects."""

from __future__ import annotations

from .model import MemoryObject


CANONICAL_STATUSES = {"canonical", "canonical_draft"}
CONTROLLED_STATUSES = {"controlled", "draft"}
GENERATED_CLASSES = {"generated_derivative", "configuration_control_wiki_page", "validation_contracts_catalog_page"}


def classify_authority(memory_object: MemoryObject) -> str:
    """Return a normalized authority class for a memory object."""

    artifact_class = memory_object.artifact_class
    authority_status = memory_object.authority_status
    registry_name = memory_object.registry_evidence.registry_name

    if artifact_class in GENERATED_CLASSES or registry_name == "derivative_registry.csv":
        return "generated_derivative"
    if registry_name == "source_registry.csv":
        if authority_status == "canonical":
            return "canonical_source"
        if authority_status == "canonical_draft":
            return "canonical_draft_source"
        if authority_status in CONTROLLED_STATUSES:
            return "controlled_source"
    if registry_name.endswith("_registry.csv"):
        return "registry_authority"
    if artifact_class in {"validation_contract", "schema"}:
        return "validation_contract"
    if artifact_class in {"config_source", "config_example"}:
        return "configuration_source"
    if artifact_class in {"agentjob", "handoff", "completion_receipt", "state_snapshot", "program_state"}:
        return "control_record"
    if authority_status == "canonical":
        return "canonical_source"
    if authority_status == "canonical_draft":
        return "canonical_draft_source"
    if authority_status in CONTROLLED_STATUSES:
        return "controlled_source"
    if ".local/" in memory_object.path or memory_object.path.startswith(".local/"):
        return "local_cache"
    return "unknown_or_unregistered"


def required_next_action(memory_object: MemoryObject) -> str:
    """Return the next required authority action for a memory object."""

    authority_class = classify_authority(memory_object)
    if authority_class in {"canonical_source", "canonical_draft_source", "controlled_source"}:
        return "inspect_canonical_source"
    if authority_class in {"registry_authority", "control_record", "configuration_source", "validation_contract"}:
        return "inspect_registry_row"
    if authority_class == "generated_derivative":
        return "reject_or_refresh_derivative"
    if authority_class == "local_cache":
        return "not_actionable_unregistered"
    return "not_actionable_unregistered"
