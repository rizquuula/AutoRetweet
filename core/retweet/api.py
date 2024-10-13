from requests import Response
from requests_oauthlib import OAuth1Session

from ..auth.oauth1 import OAuth1Service


class RetweetAPI:
    def __init__(self, oauth_service: OAuth1Service) -> None:
        self.oauth_service = oauth_service
        self.oauth_internal = OAuth1Session(
            self.oauth_service.consumer_key,
            client_secret=self.oauth_service.consumer_secret,
            resource_owner_key=self.oauth_service.access_token,
            resource_owner_secret=self.oauth_service.access_token_secret,
        )
    
    def post_retweet(self, user_id: str, tweet_id: str) -> Response:
        payload = {"tweet_id": tweet_id}
        
        response = self.oauth_internal.post(
            "https://api.twitter.com/2/users/{}/retweets".format(user_id), json=payload
        )

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
        return response
