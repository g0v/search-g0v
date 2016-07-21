import pycurl, json
import time
from io import BytesIO
import os

def curl_wrapper(url):
    userpwd = username + ":" + token
    #auth = '?client_id=allanfann&client_secret=178054dcca58aece1009258b10c860b50ea3d0fa'
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.USERPWD, userpwd)
    buffer = BytesIO()
    c.setopt(pycurl.WRITEDATA, buffer)

    c.perform()

    return (buffer.getvalue()).decode('utf-8')

#----------------------------------------


username = os.getenv('GITHUB_USER_NAME')
token = os.getenv('GITHUB_TOKEN')

if username is None or token is None:
    print("environment variable is missing: GITHUB_USER_NAME, GITHUB_TOKEN")
    exit(1)

# get awesome-g0v info
url = 'https://api.github.com/repos/g0v/awesome-g0v/contents/awesome-g0v.json'
repos_str = curl_wrapper(url)
tmp = json.loads(repos_str,encoding="utf-8")
repo_raw = curl_wrapper(tmp['download_url'])
print(repo_raw)


result = dict()
result['repos'] = json.loads(repo_raw,encoding="utf-8")
result['last_update'] = time.time()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = BASE_DIR + '/data.json'

with open(json_file, 'w') as outfile:
    json.dump(result, outfile)


print("done")
