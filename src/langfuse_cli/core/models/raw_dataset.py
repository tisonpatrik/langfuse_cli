from typing import Any

from pydantic import RootModel


class RawDatasetMatadata(RootModel[dict[str, Any]]):
    pass
