import os
from requests.models import PreparedRequest

def bearer_oauth(r: PreparedRequest) -> PreparedRequest:
    bearer_token = os.environ.get("BEARER_TOKEN")
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r
