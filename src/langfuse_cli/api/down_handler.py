import logging

from langfuse_cli.client.langfuse_client import get_langfuse_client
from langfuse_cli.services.generate_service import process_single_dataset

logger = logging.getLogger(__name__)


def resolve_dataset_names(langfuse_client) -> list[str]:
    datasets = langfuse_client.client.datasets.list().data
    if not datasets:
        raise ValueError("No datasets found in Langfuse.")

    return [ds.name for ds in datasets]


def handle_generate_command() -> int:
    try:
        langfuse_client = get_langfuse_client()

        dataset_names = resolve_dataset_names(langfuse_client)

        for dataset_name in dataset_names:
            process_single_dataset(
                langfuse_client,
                dataset_name,
            )

    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except Exception:
        logger.exception("Unexpected error during dataset generation")
        return 1

    return 0
