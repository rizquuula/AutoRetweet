from dotenv import load_dotenv
load_dotenv()

from core import AutoRetweet

# change this to username of your main accounts
main_profile_usernames = ["sama", "ylecun"]

core = AutoRetweet(
    target_accounts=main_profile_usernames,
)

core.start()