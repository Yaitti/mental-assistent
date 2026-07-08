import json
import os


def read_dialogue_history(path):
	with open(path, 'r', encoding='utf-8') as f:
		messages = json.load(f)

	return  messages
