import logging
from typing import Any

from langfuse_cli.core.models.datasets import DatasetItem, DatasetMetadata

logger = logging.getLogger(__name__)


def log_type_error(
    dataset: str, field: str, idx: int, expected: str, actual: Any
) -> None:
    logger.error(
        f"[{dataset}] Item {idx}: Invalid '{field}'. Expected {expected}, got {repr(actual)} (type={type(actual).__name__})"
    )


def is_non_empty(value: Any) -> bool:
    return bool(value) and (isinstance(value, str) or isinstance(value, (dict, list)))


def validate_item_fields(idx: int, item: Any, dataset_name: str) -> bool:
    question = getattr(item, "input", None)
    expected_output = getattr(item, "expected_output", None)
    metadata = getattr(item, "metadata", None)

    if not isinstance(metadata, dict):
        log_type_error(dataset_name, "metadata", idx, "dict", metadata)
        return False

    workspaces = metadata.get("workspaces", [])

    if not isinstance(question, (str, dict)) or not is_non_empty(question):
        log_type_error(dataset_name, "input", idx, "non-empty string or dict", question)
        return False

    if not isinstance(expected_output, (str, list)) or not is_non_empty(
        expected_output
    ):
        log_type_error(
            dataset_name,
            "expected_output",
            idx,
            "non-empty string or list",
            expected_output,
        )
        return False

    if not isinstance(workspaces, list):
        log_type_error(dataset_name, "workspaces", idx, "list of strings", workspaces)
        return False

    if not all(isinstance(w, str) for w in workspaces):
        invalid = [w for w in workspaces if not isinstance(w, str)]
        logger.error(
            f"[{dataset_name}] Item {idx}: Invalid 'workspaces' content. All items must be strings, got invalid: {invalid}"
        )
        return False

    try:
        DatasetItem(
            question=question,
            expected_output=expected_output,
            workspaces=workspaces,
        )
        logger.debug(f"[{dataset_name}] Item {idx} is valid.")
        return True
    except Exception as e:
        logger.error(
            f"[{dataset_name}] Item {idx}: Failed to construct DatasetItem: {e}"
        )
        return False


def validate_items(raw_dataset: Any, dataset_name: str) -> None:
    try:
        raw_items = getattr(raw_dataset, "items")
    except AttributeError:
        logger.error(f"[{dataset_name}] Dataset is missing 'items' attribute.")
        return
    except Exception as e:
        logger.error(f"[{dataset_name}] Unexpected error while accessing items: {e}")
        return

    if not raw_items:
        logger.warning(f"[{dataset_name}] Dataset contains no items.")
        return

    logger.info(f"[{dataset_name}] Validating {len(raw_items)} dataset items...")
    for idx, item in enumerate(raw_items):
        logger.debug(f"[{dataset_name}] Validating item {idx}...")
        validate_item_fields(idx, item, dataset_name)


def validate_metadata(raw_dataset: Any, dataset_name: str) -> None:
    try:
        metadata = getattr(raw_dataset, "metadata")
    except Exception as e:
        logger.error(f"[{dataset_name}] Could not access metadata: {e}")
        return

    if not isinstance(metadata, dict):
        log_type_error(dataset_name, "metadata", -1, "dict", metadata)
        return

    required_fields = ["name", "use_case"]
    for field in required_fields:
        if field not in metadata:
            logger.error(
                f"[{dataset_name}] Missing required metadata field '{field}'. Metadata: {repr(metadata)}"
            )

    use_case = metadata.get("use_case")
    if not isinstance(use_case, str):
        log_type_error(dataset_name, "use_case", -1, "string", use_case)
        return

    try:
        DatasetMetadata(
            name=metadata.get("name"),
            use_case=use_case,
            critical=metadata.get("critical", False),
        )
    except Exception as e:
        logger.error(f"[{dataset_name}] Failed to construct DatasetMetadata: {e}")


def validate_dataset(dataset_name: str, raw_dataset: Any) -> None:
    validate_items(raw_dataset, dataset_name)
    validate_metadata(raw_dataset, dataset_name)
