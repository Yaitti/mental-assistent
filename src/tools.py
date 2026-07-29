import json
import logger
import os


log = logger.get_logger(__name__)

def remember_fact(fact, category, save_path='data/remembered_facts.json'):
    if not os.path.exists(save_path):
        log.info("No remembered facts file found, starting fresh: %s", save_path)
        facts = {category: fact}
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(facts, f, ensure_ascii=False, indent=4)
        return f'Fact: "{fact}"  successfully remembered'
    else:
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                facts = json.load(f)
                log.info("Loaded facts from: %s", save_path)
        except(json.JSONDecodeError, OSError):
            facts = {}
            log.exception("Failed to parse remembered facts, starting new")

    try:
        facts[category] = fact
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(facts, f, ensure_ascii=False, indent=4)
        return f'Fact: "{fact}"  successfully remembered'
    except TypeError:
        log.exception("Facts contains non-serialized data, not saved")
        return f'Facts contains non-serialized data, not saved {category}'

