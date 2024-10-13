from dotenv import load_dotenv
load_dotenv()

from core import AutoRetweet


core = AutoRetweet()
core.start()