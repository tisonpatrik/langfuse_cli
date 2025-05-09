import logging

from langfuse.api.resources.commons.errors.not_found_error import NotFoundError

from langfuse_cli.core.dataset_loader import fetch_dataset
from langfuse_cli.core.file_writer import save_item_to_file
from langfuse_cli.models.cli_arguments import DatasetFilters
from langfuse_cli.models.datasets import DatasetItem, DatasetMetadata, UseCaseEnum

logger = logging.getLogger(__name__)


def validate_use_case(
    metadata: DatasetMetadata, allowed_use_cases: list[str] | None
) -> bool:
    if allowed_use_cases and metadata.use_case not in allowed_use_cases:
        return False
    return metadata.use_case in UseCaseEnum


def export_item(
    item: DatasetItem,
    index: int,
    dataset_name: str,
    use_case: str,
    filters: DatasetFilters,
) -> None:
    if not item.workspaces:
        logger.debug(f"Item {index} skipped: missing 'workspaces'.")
        return

    for workspace in item.workspaces:
        if filters.workspaces and workspace not in filters.workspaces:
            logger.debug(f"Skipping workspace '{workspace}' (filtered out).")
            continue

        filename = f"{dataset_name}_{index}.json"
        target_dir = f"datasets/{dataset_name}"
        success = save_item_to_file(workspace, use_case, item, filename, target_dir)

        if not success:
            logger.warning(
                f"Item {index} from dataset '{dataset_name}' was not saved for workspace '{workspace}'."
            )


def process_single_dataset(
    langfuse_client, dataset_name: str, filters: DatasetFilters
) -> None:
    try:
        dataset = fetch_dataset(langfuse_client, dataset_name)

        if not validate_use_case(dataset.metadata, filters.use_cases):
            logger.info(f"⏭️ Skipping dataset '{dataset_name}' due to use-case filter.")
            return

        if filters.critical and not dataset.metadata.critical:
            logger.info(f"⏭️ Skipping dataset '{dataset_name}' due to critical filter.")
            return

        for idx, item in enumerate(dataset.items):
            export_item(item, idx, dataset_name, dataset.metadata.use_case, filters)

        logger.info(f"✅ Processed dataset: {dataset_name}")

    except NotFoundError:
        logger.error(f"❌ Dataset '{dataset_name}' not found in Langfuse.")
    except ValueError as ve:
        logger.warning(f"⚠️ Skipping dataset '{dataset_name}': {ve}")
    except Exception:
        logger.exception(
            f"❌ Unexpected error during processing of dataset '{dataset_name}'"
        )
