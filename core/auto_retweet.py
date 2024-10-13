import logging
from core.auth.bearer import bearer_oauth
from core.auth.oauth1 import OAuth1Service
from core.credentials import CONSUMER_KEY, CONSUMER_SECRET
from core.retweet.api import RetweetAPI
from core.retweet.service import RetweetService
from core.stream.api import StreamAPI
from core.stream.model import Rules
from core.stream.service import StreamService
from core.user.api import UserAPI
from core.user.service import UserService


class AutoRetweet:
    
    def __init__(self) -> None:

        self.logger = self.__create_logger()
    
    
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
        
        stream_rules = Rules.from_jsonl(jsonl=[])
        stream_service.set_rules(stream_rules)
        
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

        
    