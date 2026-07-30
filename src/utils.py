import json
import sys

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
	system_prompt_path: str

@dataclass
class ModelConfig:
	model: str = "claude-sonnet-4-6"
	max_tokens: int = 20


def open_config(path):
	if not os.path.exists(path):
		raise FileNotFoundError(f"config file not found: {path}")
	with open(path, 'r', encoding='utf-8') as f:
		if path.endswith('.yaml'):
			config = yaml.safe_load(f)
		elif path.endswith(".json"):
			config = json.load(f)
		else:
			raise ValueError(f"Unsupported config format: {path}")

	log.info("Loaded config from %s", path)
	return config

def load_config(path, config_type="base"):
	if config_type == "base":
		return BaseConfig(**open_config(path))
	if config_type == "model":
		return ModelConfig(**open_config(path))


def load_system_prompt(path):
	if not os.path.exists(path):
		log.error("System prompt not found %s", path)
		sys.exit()

	with open(path, "r", encoding="utf-8") as f:
		sys_prompt = f.read()
		log.info("Loaded system prompt %s", path)
		return sys_prompt


