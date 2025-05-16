from enum import Enum

from pydantic import BaseModel


class UseCaseEnum(str, Enum):
    SEARCH = "search"
    SEARCH_ORDERED = "search_ordered"
    QUESTION_ANSWER = "question_answer"
    QUESTION_CHAIN = "question_chain"


class DatasetItem(BaseModel):
    question: str | dict[str, str]
    expected_output: str | list[str]
    workspaces: list[str]


class DatasetMetadata(BaseModel):
    critical: bool = False
    use_case: str
    name: str | None


class LangfuseDataset(BaseModel):
    name: str
    description: str | None
    metadata: DatasetMetadata
    items: list[DatasetItem]


class LangfuseDatasetConfig(BaseModel):
    name: str
    description: str | None
    metadata: DatasetMetadata
