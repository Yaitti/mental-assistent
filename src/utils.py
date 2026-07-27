import json
import logger
import os
import yaml

from dataclasses import dataclass

log = logger.get_logger(__name__)

@dataclass
class BaseConfig:
	api_key: str
	base_url: str
	dialogue_path: str
	model_config_path: str

@dataclass
class ModelConfig:
	model: str = "claude-sonnet-4-6"
	max_tokens: int = 20


def open_config(path):
	if os.path.exists(path):
		log.info(f'{path} exists')
		if path.endswith('.yaml'):
			with open(path, "r", encoding="utf-8") as f:
				config = yaml.safe_load(f)
				log.info(f'{path} was correctly opened')
				return config
		elif path.endswith(".json"):
			with open(path, "r", encoding="utf-8") as f:
				config = json.load(f)
				log.info(f'{path} was correctly opened')
				return config
		else:
			raise ValueError
	else:
		raise FileNotFoundError


def load_config(path, config_type="base"):
	if config_type == "base":
		return BaseConfig(**open_config(path))
	if config_type == "model":
		return ModelConfig(**open_config(path))


