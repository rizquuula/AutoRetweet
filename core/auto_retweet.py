from core.auth.bearer import bearer_oauth
from core.auth.oauth1 import OAuth1Service
from core.credentials import CONSUMER_KEY, CONSUMER_SECRET
from core.retweet.api import RetweetAPI
from core.retweet.service import RetweetService
from core.stream.api import StreamAPI
from core.stream.model import Rule, Rules
from core.stream.service import StreamService
from core.user.api import UserAPI
from core.user.service import UserService
import logging


class AutoRetweet:
    
    def __init__(self, target_accounts: str) -> None:
        self.target_usernames = target_accounts
        self.logger = self.__create_logger()
        
        # initiate empty rules and do conversion from account username to rules
        self.__rules = Rules()
        self.__usernames_to_rules()
    
    
    def start(self) -> None:
        oauth_service = OAuth1Service(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            log=self.logger
        )
        
        user_api = UserAPI(oauth_service)
        user_service = UserService(user_api, self.logger)
        
        user_id = user_service.read_user_id()
        
        retweet_api = RetweetAPI(oauth_service)
        retweet_service = RetweetService(retweet_api, user_id, self.logger)
        
        stream_api = StreamAPI(bearer_oauth)
        stream_service = StreamService(stream_api, self.logger)
        stream_service.delete_all_rules()
        stream_service.set_rules(self.__rules)
        stream_service.stream(retweet_service.retweet)

    
    def __create_logger(self) -> logging:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
            handlers=[
                logging.FileHandler('app.log'), 
                logging.StreamHandler(),
            ]
        )
        
        logger = logging.getLogger('AutoTweetLogger')
        return logger

    def __usernames_to_rules(self):
        for username in self.target_usernames:
            rule = Rule(
                id=None,
                value=f"from:{username}",
                tag=f"stream to user {username}"
            )
            self.__rules.add(rule)
    