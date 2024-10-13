import json
import logging
from typing import Callable
from .api import StreamAPI
from .model import Rules


class StreamService:
    
    def __init__(self, api: StreamAPI, log: logging=None) -> None:
        if api is None:
            raise Exception("StreamAPI is required")
        self.api = api
        
        if log is None: 
            log = logging
        self.log = log

    
    def read_rules(self) -> Rules:
        response = self.api.get_rules()
        
        self.log.info(json.dumps(response.json()))
        
        data = dict(response.json())
        rules_jsonl = data.get("data")
        
        return Rules.from_jsonl(rules_jsonl)


    def delete_all_rules(self) -> None:
        rules = self.read_rules()
        ids = rules.id_to_list()
        response = self.api.delete_rules(ids)
        self.log.info(json.dumps(response.json()))


    def set_rules(self, rules: Rules) -> None:
        new_rules = rules.value_to_json()
        response = self.api.post_rules(new_rules)
        self.log.info(json.dumps(response.json()))


    def stream(self, retweet_func: Callable[[str, str], None]) -> None:
        response = self.api.get_stream()
        
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                
                self.log.info(json.dumps(json_response))
                
                if retweet_func is not None:
                    retweet_func(json_response["data"]["id"])
