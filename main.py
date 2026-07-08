from urllib import response

import anthropic
import argparse
import json
import os

from httpx import request

from src import read_dialogue_history

class MemorableModel:
	def __init__(self, dialogue_path):
		self.dialogue_path = dialogue_path
		self.messages = read_dialogue_history(dialogue_path)
		self.client = anthropic.Anthropic(
			api_key="sk-kw9chzS5Y4JfNnZZvG0yB3wMxGOQnffn",
			base_url="https://api.proxyapi.ru/anthropic"
		)

	def make_response(self):
		message = self.client.messages.create(
			model="claude-sonnet-4-6",
			max_tokens=1000,
			messages=self.messages
		)

		return message.content[0].text


	def dialogue_step(self, request_text: str):
		request = {"role": "user", "content": request_text}
		self.messages.append(request)

		response = self.make_response()
		response_dict = {"assistant": "user", "content": response}
		self.messages.append(response_dict)

		with open(self.dialogue_path, 'w', encoding="utf-8") as f:
			json.dump(self.messages, f)

		return response

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-r', '--request', type=str)
	args = parser.parse_args()
	request = args.request
	session = MemorableModel("data/messages.json")

	response = session.dialogue_step(request)
	print(response)

if __name__=="__main__":
	main()