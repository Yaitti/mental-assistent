import json
import logger
import os


log = logger.get_logger(__name__)

def remember_fact(fact, category, save_path='data/remembered_facts.json'):
    if not isinstance(fact, str) or not isinstance(category, str):
        log.warning("Invalid fact/category types: %r / %r", fact, category)
        return "Could not remember, fact and category must be text."

    facts = {}
    if  os.path.exists(save_path):
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                facts = json.load(f)
        except(json.JSONDecodeError, OSError):
            log.exception("Failed to parse remembered facts, not overwriting %s", save_path)
            return "Could not remember: existing memory is unreadable."

    facts[category] = fact

    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(facts, f, ensure_ascii=False, indent=4)
    except OSError:
        log.exception("Failed to write facts file: %s", save_path)
        return "Could not remember: failed to save."

    log.info("Remembered file in category %r", category)
    return f'Remembered: "{fact}"'