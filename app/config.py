"""
Config from environment variables.
"""
import os
from dataclasses import dataclass


@dataclass
class Config:
    stage: str

    @classmethod
    def initialize_from_env(cls) -> "Config":
        """initialize config using environment variables."""
        stage = os.getenv("STAGE", "local").lower()
        return cls(stage=stage)
