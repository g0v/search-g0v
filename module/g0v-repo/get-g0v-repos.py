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

# get repos
repos = []
page = 1
while True:

    url = 'https://api.github.com/orgs/g0v/repos?page=' + str(page) + '&per_page=100'
    repos_str = curl_wrapper(url)
    #print(repos_str)
    tmp = json.loads(repos_str,encoding="utf-8")
    repos = repos + tmp
    if len(tmp) < 100:
        break
    page = page + 1


print("total repos=" + str(len(repos)))
count = 0
result = {}
result['repos'] = dict()

for repo in repos:

    print("processing repo #" + str(count))
    #print(json.dumps(repo,encoding="utf-8"))
    #exit(1)
    obj = {}
    obj['repo_owner'] = repo['owner']['login']
    obj['repo_name'] = repo['name']
    obj['repo_url'] = repo['url']
    obj['created_at'] = repo['created_at']
    obj['updated_at'] = repo['updated_at']
    obj['repo_html_url'] = repo['html_url']

    url = 'https://api.github.com/repos/' + repo['owner']['login'] + '/' + repo['name'] +  '/readme'
    readme_str = curl_wrapper(url);
    readme_obj = json.loads(readme_str,encoding="utf-8")

    if "url" in readme_obj:
        obj['readme_url'] = readme_obj['url']
        obj['readme_raw'] = curl_wrapper(readme_obj['download_url'])
    else:
        obj['readme_url'] = ''
        obj['readme_raw'] = ''

    result['repos'][obj['repo_name']] = obj

    #if count > 3:
    #    break
    count = count +1

result['last_update'] = time.time()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = BASE_DIR + '/data.json'

with open(json_file, 'w') as outfile:
    json.dump(result, outfile)

print("done")
