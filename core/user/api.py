from requests import Response
from requests_oauthlib import OAuth1Session

from ..auth.oauth1 import OAuth1Service


class UserAPI:
    def __init__(self, oauth_service: OAuth1Service) -> None:
        self.oauth_service = oauth_service
        self.oauth_internal = OAuth1Session(
            self.oauth_service.consumer_key,
            client_secret=self.oauth_service.consumer_secret,
            resource_owner_key=self.oauth_service.access_token,
            resource_owner_secret=self.oauth_service.access_token_secret,
        )
    
    def get_users_me(self, params: dict) -> Response:
        response = self.oauth_internal.get("https://api.twitter.com/2/users/me", params=params)

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        return response
