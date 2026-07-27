import anthropic
import argparse
import json
import logging
import os
import sys

from src import load_config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(f'{__name__}.log', mode="w")
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class MemorableModel:
    def __init__(self, config_path="configs/config.yaml"):
        self.config = load_config(config_path)
        self.messages = self.read_dialogue()
        self.client = anthropic.Anthropic(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )
        self.model_config = load_config(self.config.model_config_path,
                                        config_type="model")

    def read_dialogue(self):
        if os.path.exists(self.config.dialogue_path):
            logger.info("Dialogue exists")
            try:
                with open(self.config.dialogue_path, 'r', encoding="utf-8") as f:
                    dialogue = json.load(f)
                    logger.info("Dialogue successfully opened")
                    return dialogue
            except(json.JSONDecodeError, OSError):
                logger.error("Failed to parse dialogue, starting fresh")
                return []
        else:
            logger.info("Dialogue doesn't exist or Incorrect path")
            return []

    def make_response(self):
        """message = self.client.messages.create(
            model=self.model_config.model,
            max_tokens=self.model_config.max_tokens,
            messages=self.messages
        )
        logger.info("Model gave response")
        return message.content[0].text"""

        return "test response"

    def dialogue_step(self, request_text: str):
        request = {"role": "user", "content": request_text}
        self.messages.append(request)

        response = self.make_response()
        response_dict = {"role": "assistant", "content": response}
        self.messages.append(response_dict)

        with open(self.config.dialogue_path, 'w', encoding="utf-8") as f:
            json.dump(self.messages, f)

        return response


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--request', type=str)
    args = parser.parse_args()
    request = args.request
    session = MemorableModel()

    response = session.dialogue_step(request)
    print(response)


if __name__ == "__main__":
    main()
