import json
import logging
import os
import sys
import yaml

from dataclasses import dataclass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f'{__name__}.log', mode='w')
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
		logger.info(f'{path} exists')
		if path.endswith('.yaml'):
			with open(path, "r", encoding="utf-8") as f:
				config = yaml.load(f, Loader=yaml.BaseLoader)
				logger.info(f'{path} was correctly opened')
				return config
		elif path.endswith(".json"):
			with open(path, "r", encoding="utf-8") as f:
				config = json.load(path)
				logger.info(f'{path} was correctly opened')
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


