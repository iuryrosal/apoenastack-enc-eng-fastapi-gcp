from test_api.token_logic import generate_token
import requests
import os
from dotenv import load_dotenv


load_dotenv()

response = requests.get(f"{os.getenv('CLOUDRUN_URL')}/customers",
                        headers={
                                "Authorization": f"Bearer {generate_token()}"
                            }
                        )

if response.status_code in range(200, 300):
    return response.json()
else:
    raise response.raise_for_status()
