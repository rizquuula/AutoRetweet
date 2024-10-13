import json
import logging

from .api import RetweetAPI


class RetweetService:
    def __init__(self, api: RetweetAPI, user_id: str, log: logging=None) -> None:
        self.api = api
        
        if user_id is None or user_id == "":
            raise ValueError("user_id is required")
        self.user_id = user_id
        
        if log is None: 
            log = logging
        self.log = log


    def retweet(self, tweet_id: str) -> None:
        response = self.api.post_retweet(self.user_id, tweet_id)
        self.log.info(json.dumps(response.json()))
