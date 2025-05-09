import os

from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()


def get_langfuse_client() -> Langfuse:
    return Langfuse(
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        host=os.getenv("LANGFUSE_HOST"),
        environment=os.getenv("LANGFUSE_ENVIRONMENT"),
    )
