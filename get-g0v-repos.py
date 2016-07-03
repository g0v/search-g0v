import pycurl, json
import StringIO


def curl_wrapper(url):

    userpwd = 'allanfann:178054dcca58aece1009258b10c860b50ea3d0fa'
    #auth = '?client_id=allanfann&client_secret=178054dcca58aece1009258b10c860b50ea3d0fa'
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.USERPWD, userpwd)
    body = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, body.write)

    c.perform()

    return body.getvalue()

# get repos
repos = []
page = 1
while True:

    url = 'https://api.github.com/orgs/g0v/repos?page=' + str(page) + '&per_page=100'
    repos_str = curl_wrapper(url)
    tmp = json.loads(repos_str,encoding="utf-8")
    repos = repos + tmp
    if len(tmp) < 100:
        break
    page = page + 1



count = 0
result = []
print "total repos=" + str(len(repos))


for repo in repos:

    print "processing repo #" + str(count)
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

    #print readme_str

    if readme_obj.has_key('url'):
        obj['readme_url'] = readme_obj['url']
        obj['readme_raw'] = curl_wrapper(readme_obj['download_url'])
    else:
        obj['readme_url'] = ''
        obj['readme_raw'] = ''
    #print obj
    result.append(obj)

    #break
    #if count > 3:
    #    break
    count = count +1


with open('data.json', 'w') as outfile:
    json.dump(result, outfile)
