# scrapes city of chicagos food bev and hosp jobs page for lastest 100 postings
# implement radius, zip code as cmd line args

import urllib
import datetime
from lxml.html import parse
import sys

class craigsCrawler():

  def __init__(self):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date'
    self. blurb_limit = 50 # amount of text to print to console


def get_page(url):
  try:
    print 'getting page'
    handle = urllib.urlopen(url)
    page = parse(handle).getroot()
    return page
  except IOError as e:
    print 'problem getting page. are you connected to the internet?'
    return None
  except UnicodeEncodeError:
    print 'format error'
    return None
  except UnicodeError:
    print 'format error'
    return None

def main():
  c = craigsCrawler()
  html = get_page(c.url)
  if html != None:
    pls = html.find_class('pl')
    for pl in pls:
      for thing in pl:
        if thing.tag == 'time': # looking for tag -time- with attr -datetime- 
          time_posted = thing.get('datetime') # use get which takes attr and returns the value
        if thing.tag == 'a': # also looking for the job description title text
          job_text = thing.text 
          if len(job_text) > c.blurb_limit:
            blurb = job_text[:c.blurb_limit]
          else:
            blurb = job_text
      print blurb + ' posted on ' + time_posted

main()

