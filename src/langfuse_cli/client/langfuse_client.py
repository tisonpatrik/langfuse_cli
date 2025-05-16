import logging
import os

from dotenv import load_dotenv
from langfuse import Langfuse

logger = logging.getLogger(__name__)

load_dotenv()

host = os.getenv("LANGFUSE_HOST")
public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
secret_key = os.getenv("LANGFUSE_SECRET_KEY")


def __env_vars_are_in_env() -> bool:
    missing = []

    if not host:
        missing.append("LANGFUSE_HOST")
    if not public_key:
        missing.append("LANGFUSE_PUBLIC_KEY")
    if not secret_key:
        missing.append("LANGFUSE_SECRET_KEY")

    if missing:
        logger.error(
            f"Missing required Langfuse environment variables: {', '.join(missing)}. "
            "Please ensure these variables are set in your environment or .env file."
        )
        return False

    return True


def get_langfuse_client() -> Langfuse:
    env_ok = __env_vars_are_in_env()
    if not env_ok:
        raise RuntimeError(
            "Langfuse client authentication failed: missing environment variables."
        )

    client = Langfuse(
        secret_key=secret_key,
        public_key=public_key,
        host=host,
    )

    try:
        client.auth_check()
    except Exception as e:
        logger.error(
            "Langfuse authentication failed.\n"
            "- Check your environment variables\n"
            "- Check your network connectivity\n"
            "- Check your Langfuse account access\n"
            "- If all above is OK, Langfuse server may be down."
        )
        raise RuntimeError("Langfuse client authentication failed.") from e

    return client
