import logging
from argparse import Namespace

from langfuse_cli.client.langfuse_client import get_langfuse_client
from langfuse_cli.core.generate_service import process_single_dataset
from langfuse_cli.models.cli_arguments import (
    DatasetFilters,
    DatasetGeneratorArgs,
)

logger = logging.getLogger(__name__)


def _parse_generator_args(args: Namespace) -> DatasetGeneratorArgs:
    try:
        return DatasetGeneratorArgs(
            filters=DatasetFilters(
                workspaces=args.workspaces,
                use_cases=args.use_cases,
                critical=args.critical,
            ),
            datasets=args.datasets,
        )
    except Exception as e:
        raise ValueError(f"Failed to parse generator arguments: {str(e)}")


def resolve_dataset_names(
    langfuse_client, generator_args: DatasetGeneratorArgs
) -> list[str]:
    if generator_args.datasets:
        return generator_args.datasets

    datasets = langfuse_client.client.datasets.list().data
    if not datasets:
        raise ValueError("No datasets found in Langfuse.")

    return [ds.name for ds in datasets]


def handle_generate_command(args) -> int:
    try:
        generator_args = _parse_generator_args(args)
        langfuse_client = get_langfuse_client()

        dataset_names = resolve_dataset_names(langfuse_client, generator_args)

        for dataset_name in dataset_names:
            process_single_dataset(
                langfuse_client, dataset_name, generator_args.filters
            )

    except ValueError as e:
        logger.error(f"Input error: {e}")
        return 1
    except Exception:
        logger.exception("Unexpected error during dataset generation")
        return 1

    return 0
