import logging
from typing import Any

from langfuse_cli.core.models.datasets import DatasetItem, DatasetMetadata

logger = logging.getLogger(__name__)


def parse_raw_items(raw_items: list[Any], dataset_name: str) -> None:
    logger.info(f"[{dataset_name}] Validating {len(raw_items)} dataset items...")

    for idx, item in enumerate(raw_items):
        logger.debug(f"[{dataset_name}] Validating item {idx}...")

        question = getattr(item, "input", None)
        expected_output = getattr(item, "expected_output", None)
        metadata = getattr(item, "metadata", None)

        if not isinstance(metadata, dict):
            logger.error(
                f"[{dataset_name}] Item {idx}: Invalid 'metadata'. Expected dict, got {repr(metadata)} (type={type(metadata).__name__})"
            )
            continue

        workspaces = metadata.get("workspaces", [])

        if not isinstance(question, (str, dict)) or not question:
            logger.error(
                f"[{dataset_name}] Item {idx}: Invalid 'input'. Expected non-empty string or dict, got {repr(question)} (type={type(question).__name__})"
            )
            continue

        if not isinstance(expected_output, (str, list)) or not expected_output:
            logger.error(
                f"[{dataset_name}] Item {idx}: Invalid 'expected_output'. Expected non-empty string or list, got {repr(expected_output)} (type={type(expected_output).__name__})"
            )
            continue

        if not isinstance(workspaces, list):
            logger.error(
                f"[{dataset_name}] Item {idx}: Invalid 'workspaces'. Expected list of strings, got {repr(workspaces)} (type={type(workspaces).__name__})"
            )
            continue

        if not all(isinstance(w, str) for w in workspaces):
            bad = [w for w in workspaces if not isinstance(w, str)]
            logger.error(
                f"[{dataset_name}] Item {idx}: Invalid 'workspaces' content. All items must be strings, got invalid: {bad}"
            )
            continue

        try:
            DatasetItem(
                question=question,
                expected_output=expected_output,
                workspaces=workspaces,
            )
            logger.debug(f"[{dataset_name}] Item {idx} is valid.")
        except Exception as e:
            logger.error(
                f"[{dataset_name}] Item {idx}: Failed to construct DatasetItem: {e}"
            )


def validate_dataset(raw_dataset: Any) -> None:
    dataset_name = getattr(raw_dataset, "name", "<unknown>")

    try:
        raw_items = getattr(raw_dataset, "items")
        if not raw_items:
            logger.warning(f"[{dataset_name}] Dataset contains no items.")
        else:
            parse_raw_items(raw_items, dataset_name)
    except AttributeError:
        logger.error(f"[{dataset_name}] Dataset is missing 'items' attribute.")
    except Exception as e:
        logger.error(f"[{dataset_name}] Unexpected error while validating items: {e}")

    try:
        raw_metadata = getattr(raw_dataset, "metadata")
        if not isinstance(raw_metadata, dict):
            logger.error(
                f"[{dataset_name}] Invalid 'metadata'. Expected dict, got {repr(raw_metadata)} (type={type(raw_metadata).__name__})"
            )
            return

        required_fields = ["name", "use_case"]
        for field in required_fields:
            if field not in raw_metadata:
                logger.error(
                    f"[{dataset_name}] Missing required metadata field '{field}'. Metadata: {repr(raw_metadata)}"
                )

        use_case = raw_metadata.get("use_case")
        if not isinstance(use_case, str):
            logger.error(
                f"[{dataset_name}] Invalid 'use_case'. Expected string, got {repr(use_case)} (type={type(use_case).__name__})"
            )
            return

        DatasetMetadata(
            name=raw_metadata.get("name"),
            use_case=use_case,
            critical=raw_metadata.get("critical", False),
        )

    except Exception as e:
        logger.error(f"[{dataset_name}] Failed to validate metadata: {e}")
