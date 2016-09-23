# scrapes craigslist's city of chicagos food bev and hosp jobs page for lastest 100 postings
# implement radius, zip code, and as cmd args

import urllib
import time
from lxml.html import parse

class craigsCrawler():

  def __init__(self):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date'
    self. blurb_limit = 60 # amount of text to print to console

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
    pls = html.find_class('pl') # inner most class row row posting with class name
    for pl in pls:
      for thing in pl:
        if thing.tag == 'time': # looking for tag -time- with attr -datetime- 
          date_posted = thing.get('datetime') # use get which takes attr and returns the value
          parsed_date = c.parse_date(date_posted) # that day
          today = time.strftime('%d') # this day
          if parsed_date[0] == today: # if they are the same
            jobs_today += 1 # it was posted today
        if thing.tag == 'a': # also looking for the job description title text
          job_text = thing.text 
          blurb = job_text[:c.blurb_limit] # crop it to the blurb limit
      print blurb + ' posted on ' + date_posted
  print str(jobs_today) + ' jobs posted today'

main()

