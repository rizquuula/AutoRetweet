import logging
import os
import pickle
from requests_oauthlib import OAuth1Session


class OAuth1Service:
    
    def __init__(self, consumer_key: str, consumer_secret: str, path: str='default_oauth1.pkl', log: logging=None) -> None:
        if consumer_key is None or consumer_key == "":
            raise ValueError("consumer_key is required")
        
        if consumer_secret is None or consumer_secret == "":
            raise ValueError("consumer_secret is required")
        
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        
        if log is None: 
            log = logging
        self.log = log
        
        self.resource_owner_key = None
        self.resource_owner_secret = None
        self.verifier = None
        self.access_token = None
        self.access_token_secret = None
        
        self.path = path
        self.__load_oauth1()
        self.__save_to_file()
    
    
    def __save_to_file(self) -> None:
        with open(self.path, 'wb') as f:
            pickle.dump(self, f)
    
    
    def __load_oauth1(self):
        if not os.path.isfile(self.path):
            self.__auth()
            return

        loaded_oauth1 = None
        with open(self.path, 'rb') as f:
            loaded_oauth1: OAuth1Service = pickle.load(f)
            
        if loaded_oauth1.consumer_key != self.consumer_key:
            self.__auth()
            return
        
        self.resource_owner_key = loaded_oauth1.resource_owner_key
        self.resource_owner_secret = loaded_oauth1.resource_owner_secret
        self.verifier = loaded_oauth1.verifier
        self.access_token = loaded_oauth1.access_token
        self.access_token_secret = loaded_oauth1.access_token_secret


    def __auth(self):
        self.__get_consumer_token()
        self.__get_access_token()
    
    
    def __get_consumer_token(self):
        # Get request token
        request_token_url = "https://api.twitter.com/oauth/request_token"
        
        oauth = OAuth1Session(
            client_key=self.consumer_key, 
            client_secret=self.consumer_secret,
        )
        
        headers = {
            "oauth_callback": "oob",
        }

        try:
            fetch_response = oauth.fetch_request_token(request_token_url, headers=headers)
        except ValueError as e:
            print(
                "There may have been an issue with the consumer_key or consumer_secret you entered."
            )
            raise e

        self.resource_owner_key = fetch_response.get("oauth_token")
        self.resource_owner_secret = fetch_response.get("oauth_token_secret")
        self.log.info(f"Got OAuth resource_owner_key: {self.resource_owner_key}")
        self.log.info(f"Got OAuth resource_owner_secret: {self.resource_owner_key}")
        
        self.__do_authorization(oauth)
    
    
    def __do_authorization(self, oauth: OAuth1Session):
        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the oauth_verifier in the redirect URL here: ")
        self.verifier = verifier


    def __get_access_token(self):
        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.resource_owner_key,
            resource_owner_secret=self.resource_owner_secret,
            verifier=self.verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        self.access_token = oauth_tokens["oauth_token"]
        self.access_token_secret = oauth_tokens["oauth_token_secret"]