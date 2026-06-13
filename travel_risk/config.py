import os
from typing import Dict, Any, Optional, List
from 




TFL_BASE_URL = "https://api.tfl.gov.uk"
TFL_APP_KEY = os.getenv("TFL_APP_KEY")
FROM_LOCATION = "Stratford"
TO_LOCATION = "Paddington"
COMMUTE_LINES = ["central", "jubilee", "elizabeth"]
POLL_SECONDS = 30
TOPIC = "commute-risk"