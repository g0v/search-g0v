import pycurl, json
import time
from io import BytesIO
import os
import html2text
from datetime import datetime, timedelta
def curl_wrapper(url):

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    buffer = BytesIO()
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()

    return (buffer.getvalue()).decode('utf-8')

#----------------------------------------

date = "2013-07-26"
count = 10
results = {}
results['logs']= {}
while True:
    url = "https://logbot.g0v.tw/channel/g0v.tw/" + date
    print(url)
    try:
        str = curl_wrapper(url)
        content = html2text.html2text(str)
        done = True
        print("curl ok")
    except:
        content = ""
        done = False
        print("curl fail")

    tmp = datetime.strptime(date, "%Y-%m-%d")
    tmp_date = tmp + timedelta(days=1)
    date = tmp_date.strftime("%Y-%m-%d")
    results['logs'][date] = {
        "date": date,
        "url": url,
        "content": content,
        "done": done
    }

    #obj= {
    #    "date": date,
    #    "url": url,
    #    "content": content
    #}
    #print(obj)
    if tmp_date >= datetime.today():
        break

    count = count - 1
    if count <= 0:
        break


results['last_update'] = time.time()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_file = BASE_DIR + '/data.json'

with open(json_file, 'w') as outfile:
    json.dump(results, outfile)

print("get-irc-log done")
