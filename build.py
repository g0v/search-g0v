# coding=utf-8
#!/usr/bin/python

import os

# common index directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
indexdir = BASE_DIR + '/indexdir'


# hackpad backup
# update hackpad backup data from submodule (https://github.com/g0v-data/hackpad-backup-g0v)
os.system('git submodule update --init')
# update hackfoldr g0v
os.system('python3 module/hackfoldr/make_index.py -o %s' % indexdir)
os.system('python3 module/hackpad-backup/make_index.py -o %s' % indexdir)

# g0v-repo
os.system('python3 module/g0v-repo/make_index.py -o %s'  % indexdir)

# update IRCLog
os.system('python3 module/irc-log/make_index.py -o %s' % indexdir)

# update awesome g0v
os.system('python3 module/awesome-g0v/make_index.py -o %s' % indexdir)
