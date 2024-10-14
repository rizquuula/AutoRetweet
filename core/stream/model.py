from typing import List


class Rule:
    def __init__(self, id: str, value: str, tag: str) -> None:
        self.id = id
        self.value = value
        self.tag = tag
    
    @staticmethod
    def from_json(json: dict) -> "Rule":
        id = json.get("id")
        value = json.get("value")
        tag = json.get("tag")
        return Rule(id, value, tag)
        
    def value_to_json(self) -> dict:
        return {"value": self.value, "tag": self.tag}


class Rules:
    def __init__(self, rules: List[Rule]) -> None:
        self.rules = rules
    
    @staticmethod
    def from_jsonl(jsonl: List[dict]) -> "Rules":
        rules = [Rule.from_json(json) for json in jsonl]
        return Rules(rules)
    
    def value_to_json(self) -> List[dict]:
        return [r.value_to_json() for r in self.rules]
    
    def id_to_list(self) -> List[str]:
        return [r.id for r in self.rules]

    def add(self, rule: Rule) -> None:
        self.rules.append(rule)
