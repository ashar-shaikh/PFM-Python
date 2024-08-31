from dotenv import load_dotenv
import os


class Flags:
    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self._load_env_vars()

    def _load_env_vars(self):
        load_dotenv(self.env_file)

    def get(self, key, default=None, description=""):
        value = os.getenv(key.upper(), default)
        if value is None:
            raise ValueError(f"Environment variable '{key.upper()}' is not set. {description}")
        return value
