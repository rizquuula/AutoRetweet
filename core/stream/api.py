from requests import PreparedRequest, Response
from typing import Callable, List
import logging
import requests


class StreamAPI:
    
    def __init__(self, bearer_oauth: Callable[[PreparedRequest], PreparedRequest], log: logging=None) -> None:
        if bearer_oauth is None:
            raise ValueError("bearer_oauth is required")
        self.bearer_oauth = bearer_oauth
        
        if log is None: 
            log = logging
        self.log = log


    def get_rules(self) -> Response:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", auth=self.bearer_oauth
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return response


    def delete_rules(self, ids: List[str]) -> Response:
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return response


    def post_rules(self, rules: dict) -> Response:
        payload = {"add": rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            auth=self.bearer_oauth,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return response

    def get_stream(self) -> Response:
        params = {
            "tweet.fields": "conversation_id,id,in_reply_to_user_id"
        }
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream", params=params, auth=self.bearer_oauth, stream=True,
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return response