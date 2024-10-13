import json
import logging

from .api import UserAPI


class UserService:
    def __init__(self, api: UserAPI, log: logging=None) -> None:
        self.api = api
        
        if log is None: 
            log = logging
        self.log = log


    def read_user_id(self) -> str:
        fields = "id"
        params = {"user.fields": fields}

        response = self.api.get_users_me(params)
        json_response = response.json()

        self.log.info(json.dumps(json_response))
        
        return json_response['data']['id']