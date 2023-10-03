
import requests
import json
import sys
import pandas as pd

inpt_df = pd.read_csv("post_sample_csv.csv")
headers = {'Content-Type': 'application/json'}

list_text = inpt_df['oupt'].tolist()
for i in list_text:
    # Create body for testing
    post_body = {
        "from_lang": "es",
        "to_lang": "en",
        "text": i
    }
    # Make request
    r = requests.post("http://192.168.50.21:4567/translation/single", json = post_body)

    # Stdout
    oupt_dict = {'inpt': post_body['text'], 'oupt': r.json()['data']['response']}
    #oupt_df = pd.DataFrame(oupt_dict)
    #oupt_df.to_csv("post_sample_csv.csv", index = False, encoding="utf-8")
    sys.stdout.write(f"Status Code: {r.status_code} \nResponse: {r.json()['data']['response']}\n")