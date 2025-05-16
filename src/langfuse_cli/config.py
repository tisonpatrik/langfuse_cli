from pydantic import BaseModel


class Config(BaseModel):
    datasets_target_dir: str
