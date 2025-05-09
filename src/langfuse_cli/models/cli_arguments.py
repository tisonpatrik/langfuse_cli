from pydantic import BaseModel


class DatasetFilters(BaseModel):
    workspaces: list[str] | None = None
    use_cases: list[str] | None = None
    critical: bool | None = False


class DatasetGeneratorArgs(BaseModel):
    filters: DatasetFilters
    datasets: list[str] | None = None
