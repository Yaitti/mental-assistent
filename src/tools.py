import json
import logger
import os


log = logger.get_logger(__name__)


def remember_fact(name, content, save_path):
    fact = {name: content}
    if not os.path.exists(save_path):
        log.info("No remembered facts file found, starting fresh")
        facts = []
    else:
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                facts = json.load(f)
                log.info("Loaded facts from %s", save_path)
        except(json.JSONDecodeError, OSError):
            facts = []
            log.exception("Failed to parse remembered facts, starting new")

    facts.append(fact)
    print(facts)
    try:
        with open(save_path, 'r', encoding='utf-8') as f:
            json.dump(facts, f, ensure_ascii=False, indent=4)
        return True
    except TypeError:
        log.exception("Facts contains non-serialized data, not saved")
        return False

