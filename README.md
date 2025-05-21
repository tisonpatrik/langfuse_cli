# Langfuse CLI

Langfuse CLI is a helper tool for downloading and uploading evaluation datasets from your Langfuse account.

## Installation

1. **Python**: ensure Python 3.12 or newer is available.
2. **uv**: install the [uv](https://github.com/astral-sh/uv) tool, e.g. `pip install uv`.
3. Install project dependencies:
   ```bash
   uv pip install -e .
   ```
   You can replace `uv` with `pip` if you prefer a standard virtual environment.

## Environment variables

Provide the following variables either in your environment or a `.env` file so the CLI can authenticate with Langfuse:

```
LANGFUSE_HOST=<your-langfuse-host>
LANGFUSE_PUBLIC_KEY=<your-public-key>
LANGFUSE_SECRET_KEY=<your-secret-key>
```

## Usage

The CLI supports two commands. Use one of `--down` or `--up`.

### Download datasets

```bash
uv run langfuse-cli -d
```

This downloads all datasets from Langfuse into the directory specified by `datasets_target_dir` (default `datasets`) in `config.yaml`.

### Upload datasets

```bash
uv run langfuse-cli -u
```

This reads dataset configuration files from `datasets/configs` and uploads them to Langfuse.

## Configuration

`config.yaml` contains the path where datasets are stored locally:

```yaml
datasets_target_dir: datasets
```

Adjust this value if you want the files in a different location.
