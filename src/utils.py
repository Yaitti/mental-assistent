import json
import os
import yaml

from dataclasses import dataclass


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
		print("config opened")
		if path.endswith('.yaml'):
			print("config is yaml")
			with open(path, "r", encoding="utf-8") as f:
				config = yaml.load(f, Loader=yaml.BaseLoader)
				return config
		elif path.endswith(".json"):
			with open(path, "r", encoding="utf-8") as f:
				config = json.load(path)
			return config
		else:
			print("Incorrect config type")
	else:
		print("path doesn't exist")


def load_config(path, config_type="base"):
	if config_type == "base":
		return BaseConfig(**open_config(path))
	if config_type == "model":
		return ModelConfig(**open_config(path))

def read_dialogue_history(path):
	with open(path, 'r', encoding='utf-8') as f:
		messages = json.load(f)

	return  messages
