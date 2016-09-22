# scrapes city of chicagos food bev and hosp jobs page for lastest 100 postings
# implement radius, zip code, as cmd args

import urllib
import time
from lxml.html import parse
import sys

class craigsCrawler():

  def __init__(self):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date'
    self. blurb_limit = 50 # amount of text to print to console

  def parse_date(self, date_string):
    split1 = date_string.split('-')
    year = split1[0]
    month = split1[1]
    split2 = split1[2]
    split2 = split2.split(' ')
    day = split2[0]
    time = split2[1] # 24:00
    return [day, month, year, time]


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
  jobs_today = 0
  html = get_page(c.url)
  if html != None:
    pls = html.find_class('pl')
    for pl in pls:
      for thing in pl:
        if thing.tag == 'time': # looking for tag -time- with attr -datetime- 
          date_posted = thing.get('datetime') # use get which takes attr and returns the value
          parsed_date = c.parse_date(date_posted) # then
          today = time.strftime('%d') #now
          if parsed_date[0] == today:
            jobs_today += 1
        if thing.tag == 'a': # also looking for the job description title text
          job_text = thing.text 
          if len(job_text) > c.blurb_limit:
            blurb = job_text[:c.blurb_limit]
          else:
            blurb = job_text
      print blurb + ' posted on ' + date_posted
  print str(jobs_today) + ' jobs posted today'

main()

