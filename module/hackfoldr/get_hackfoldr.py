# coding=utf-8
import os

from os import walk
import time
import sys
import re
import git
import json
import html2text
import urllib
import urllib.request
# import gsheet2json

def clean_json(raw_data):
    entries = raw_data['feed']['entry']
    cols = [x for x in entries[0] if x.startswith('gsx$')]
    data = []
    for entry in entries:
        row = {}
        for col in cols:
            row[col[4:]] = entry[col]['$t']
        data.append(row)
    # return json.JSONEncoder().encode(data)
    return data


sys.setrecursionlimit(200000)
# g = git.cmd.Git('hackpad-backup-g0v')
# g.execute(["git", "submodule", "update"])
# print('pull from hackpad-backup-g0v: done')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
	last_update = open('last_update.txt').read()
except:
	last_update = 0

with open('hackpad-backup-g0v/pads.json') as data_file: 
	data = json.load(data_file)

git_ff = {}
for pad in data:
	git_ff[pad['padid']] = pad

try:
	# 讀取 last_pads.json ++
	with open('last_pads.json') as lp: 
		last_pads = json.load(lp)
except:
	last_pads = {}

ff = {}
for k,v in git_ff.items():
	if k not in last_pads:
		ff[k] = git_ff[k]
	if(v['last_backup_time'] > float(last_update)):
		ff[k] = git_ff[k]

print("總共 " + str(len(data)) + " 個 pad")
print("上次建立時間：" + time.ctime(float(last_update)))
print("需要更新數量：" + str(len(ff)))
print("開始抓取所有 hackfoldr 連結")
print("===================================")

all_url = {}
i = 0
for new_padID in ff:
	print(new_padID)

	html = open('hackpad-backup-g0v/' + new_padID + '.html').read()
	all_text = html2text.html2text(html)
	all_text = all_text.strip()
	all_text = re.sub('[\s+]', '', all_text)
	urls = re.findall('http[s]?://(?:beta\.)?hackfoldr.org/[0-9a-zA-Z_-]+', all_text)
	print(i)
	i =  i + 1

	for us in urls:
		
		tmp_urls = []
		get_id = urllib.parse.urlsplit(us)
		this_hackfoldrs = re.split("\/", get_id.path)
		this_hackfoldr = this_hackfoldrs[1]

		if this_hackfoldr != "about":

			try:
				if all_url[this_hackfoldr]:
					tmp_urls = all_url[this_hackfoldr]['metion']
					if new_padID not in tmp_urls:
						tmp_urls.append(new_padID)
					all_url[this_hackfoldr]['metion'] = tmp_urls
			
			except:
				new_hackfoldr = {}
				new_hackfoldr['id'] = this_hackfoldr
				tmp_urls.append(new_padID)
				new_hackfoldr['metion'] = tmp_urls
				new_hackfoldr['text'] = all_text
				all_url[this_hackfoldr] = new_hackfoldr
		
		print(this_hackfoldr)

all_data = {}
all_title = {}

print('hackfoldr 數量：')
print(len(all_url))

for u in all_url:	
	ethercalc_url = "https://ethercalc.org/_/" + u + "/csv.json"
	k = u
	data = {}
	gsheet = ''
	print("============================================================================================")
	print(ethercalc_url)

	url_id = u
	url = "https://spreadsheets.google.com/feeds/list/" + \
	url_id + "/od6/public/values?alt=json"

	# url = 'https://docs.google.com/feeds/download/spreadsheets/Export?key='+ url_id +'&exportFormat=json&gid=0'

	try:
		response = urllib.request.urlopen(url)
		raw_data = json.loads(response.read().decode('utf8'))
		data = clean_json(raw_data)
		all_data[u] = data

		ii = 0
		d = {}
		for d in data:
			print(d)
			if(len(d) > 1):
				this_data = {}
				this_data['url'] = 'http://beta.hackfoldr.org/' + u
				this_data['title'] = d['title'].lstrip()
				this_data['metion'] = all_url[u]['metion']
				all_links = []
				for dd in data:
					if dd['title'] is not "" and '#' not in dd['title']:
						all_links.append(dd['title'].lstrip())
						item_title = dd['title'].lstrip()
						all_links.append(item_title)
						print(dd['title'])
				this_data['links'] = all_links
				all_title[k] = this_data
				break
			else:
				this_data = {}
				this_data['url'] = 'http://beta.hackfoldr.org/' + u
				this_data['title'] = k
				this_data['metion'] = all_url[u]['metion']		
				all_title[k] = this_data



	except urllib.error.URLError:
		try:
			response = urllib.request.urlopen(ethercalc_url)
			content = response.read()
			data = json.loads(content.decode('utf8'))
			all_data[u] = data

			ii = 0
			d = {}
			for d in data:
				print(d)
				if(len(d) > 1):
					if d[0] is "" and d[1] is not "" and "#" not in d[1]:
						this_data = {}
						this_data['url'] = 'http://beta.hackfoldr.org/' + u
						this_data['title'] = d[1].lstrip()
						this_data['metion'] = all_url[u]['metion']
						all_links = []	
						for dd in data:
							if dd[1] is not "" and '#' not in dd[1]:
								item_title = dd[1].lstrip()
								all_links.append(item_title)
								print(dd[1])
						this_data['links'] = all_links
						all_title[k] = this_data
						break
					else:
						if(ii >= 2):
							this_data = {}
							this_data['url'] = 'http://beta.hackfoldr.org/' + u
							this_data['metion'] = all_url[u]['metion']
							all_links = []	
							for dd in data:							
								if dd[1] is not "" and '#' not in dd[1]:
									this_data['title'] = dd[1].lstrip()										
									item_title = dd[1].lstrip()
									all_links.append(item_title)
									print(dd[1])
							this_data['links'] = all_links
							all_title[k] = this_data
							break
						else:
							print("next row")
							ii = ii + 1
				else:
					this_data = {}
					this_data['url'] = 'http://beta.hackfoldr.org/' + u
					this_data['title'] = k
					this_data['metion'] = all_url[u]['metion']
					all_title[k] = this_data

		except:
			this_data = {}
			this_data['url'] = 'http://beta.hackfoldr.org/' + u
			this_data['title'] = u
			this_data['links'] = ['empty table']
			this_data['metion'] = all_url[u]['metion']
			all_title[k] = this_data
			print('failed to open url')			
			print("error")


# print("done")
print(all_title)
print(len(all_title))

with open(BASE_DIR + '/hackfoldr.json', 'w') as outfile:
    json.dump(all_title, outfile)



