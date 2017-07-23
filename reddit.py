#!/usr/bin/env python2.7

import os
import sys
import requests
import re

def usage():
  print '''Usage: reddit.py  [ -f FIELD -s SUBREDDIT ] regex
	     -f FIELD	      Which field to search (default: title)
	     -n LIMIT	      Limit number of articles to report (default: 10)
	     -s SUBREDDIT     Which subreddit to search (default: linux)'''
  sys.exit()

field = "title"
limit = 10
subreddit = "linux"

args = sys.argv[1:]

while len(args) and args[0].startswith('-') and len(args[0]) > 1:
  arg = args.pop(0)
  if arg == '-f':
    field = args.pop(0)
  elif arg == '-n':
    limit = int(args.pop(0))
  elif arg == '-s':
    subreddit = args.pop(0)
  else:
    usage()

if len(args):
  regex = args.pop(0)
else:
  regex = ''

url = 'https://www.reddit.com/r/' + subreddit + '/.json'
headers = {'user-agent': 'reddit-{}'.format(os.environ['USER'])}
r = requests.get(url, headers=headers)

dic = r.json()['data']['children']

count = 1
for i in dic:
  if field in i['data'].keys():
    check = i['data'][field]
    find = re.findall(regex, check)
    if regex == '' or len(find) > 0:
      title = i['data']['title']
      num = str(count) + "."
      print num, "Title: ", title
      author = i['data']['author']
      print "Author:   ", author
      link = "https://www.reddit.com" + i['data']['permalink']
      print "Link:     ", link
      r = requests.get('http://is.gd/create.php', params = { 'format': 'json', 'url': link})
      short = r.json()['shorturl']
      print "Short:    ", short, "\n"
      count += 1
    if count > limit:
      break
  else:
    print "Invalid field:", field
    sys.exit(1)

