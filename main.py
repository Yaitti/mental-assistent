import anthropic
import argparse
import json
import logger
import os
import re

log = logger.set_app_lvl_logger()

from src import load_config, remember_fact, load_system_prompt, parse_tools

class MemoryAssistant:
    def __init__(self, config_path="configs/config.yaml"):
        self.config = load_config(config_path)
        self.messages = self.read_dialogue()
        self.client = anthropic.Anthropic(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )
        self.model_config = load_config(self.config.model_config_path,
                                        config_type="model")
        self.sys_prompt = load_system_prompt(self.config.system_prompt_path)

    def read_dialogue(self):
        if not os.path.exists(self.config.dialogue_path):
            log.info("No dialogue file found, starting new")
            return []
        try:
            with open(self.config.dialogue_path, 'r', encoding="utf-8") as f:
                dialogue = json.load(f)
            log.info("Loaded %d messages from dialogue file", len(dialogue))
            return dialogue
        except(json.JSONDecodeError, OSError):
            log.error("Failed to parse dialogue")
            raise

    def generate_response(self):
        message = self.client.messages.create(
            model=self.model_config.model,
            max_tokens=self.model_config.max_tokens,
            system=self.sys_prompt,
            messages=self.messages
        )
        log.info("Model returned response")
        return message.content[0].text

        #return 'и ты не один с этим.\n<tool_call>\n{"name": "remember_fact", "arguments": {"fact": "У пользователя СДВГ (синдром дефицита внимания и гиперактивности)", "category": "диагноз"}}\n</tool_call>'

    def tool_call(self, calls):
        tools_result = {}
        for call in calls:
            tool_func = globals()[call["name"]]
            log.info("Executing tool '%s'", call["name"])
            tool_res = tool_func(**call["arguments"])
            tools_result[call["name"]] = tool_res
        return tools_result

    def dialogue_step(self, request_text: str):
        final_response = []
        request = {"role": "user", "content": request_text}
        self.messages.append(request)

        response = self.generate_response()
        final_response.append(response)

        calls = parse_tools(response)
        while calls:
            log.info(f'Found tools from response: {[call["name"] for call in calls]}')
            tools_response = self.tool_call(calls)

            assistant_message = {"role": "assistant", "content": response}
            tool_message = {"role": "user", "content": f'<tool_result>: {str(tools_response)}'}
            self.messages.extend([assistant_message, tool_message])

            response = self.generate_response()
            final_response.append(response)
            calls = parse_tools(response)
        
            return '\n'.join(final_response)

        assistant_message = {"role": "assistant", "content": response}
        self.messages.append(assistant_message)

        with open(self.config.dialogue_path, 'w', encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)

        return response


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--request', type=str, required=True)
    args = parser.parse_args()
    request = args.request
    session = MemoryAssistant()
    response = session.dialogue_step(request)
    print(response)

if __name__ == "__main__":
    main()
