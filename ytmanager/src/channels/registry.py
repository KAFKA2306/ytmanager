from pathlib import Path
from typing import Dict
import yaml
from pydantic import BaseModel


class AnalyticsConfig(BaseModel):
    enabled: bool = True
    metrics: list[str]
    lookback_days: int = 7


class OptimizerConfig(BaseModel):
    enabled: bool = True
    auto_tune: bool = False
    ab_test_ratio: float = 0.1
    feedback_interval: str = "daily"
    min_sample_size: int = 10


class ChannelConfig(BaseModel):
    project_path: str
    youtube_channel_id: str
    schedule: str
    analytics: AnalyticsConfig
    optimizer: OptimizerConfig
    description: str = ""


class ChannelRegistry:
    def __init__(self, config_path: str = "config/channels.yaml"):
        self.config_path = Path(config_path)
        self.channels: Dict[str, ChannelConfig] = {}
        self.load()

    def load(self):
        with open(self.config_path) as f:
            data = yaml.safe_load(f)
        for name, config in data["channels"].items():
            self.channels[name] = ChannelConfig(**config)

    def get(self, name: str) -> ChannelConfig:
        return self.channels[name]

    def list(self) -> list[str]:
        return list(self.channels.keys())
