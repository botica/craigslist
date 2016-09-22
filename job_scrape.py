# scrapes city of chicagos food bev and hosp jobs page for lastest 100 postings

# implement radius, zip code as cmd line args

import urllib
import time
from lxml.html import parse
import sys

class craigsCrawler():

  def __init__(self):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date' #food bev hosp city recent
    self. blurb_limit = 50 #amt of txt 2 dsply 2 cnsl


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

def main(): # scrapes a page, parses for some shit, prints it out
  c = craigsCrawler()
  html = get_page(c.url) # try to get the page
  if html != None:
    pls = html.find_class('pl') # innermost classname for a post listing
    for pl in pls: # so we have to iterate
      for thing in pl: # two levels down
        if thing.tag == 'time': # looking for tag -time- with attr -datetime- 
          time_posted = thing.get('datetime') # use get which takes attr and returns the value
        if thing.tag == 'a': # also looking for the job description title text
          job_text = thing.text 
          blurb = '' # create a string to append characters to (implement proerp way)
          if len(job_text) > c.blurb_limit:
            for i in range(0, c.blurb_limit - 1):
              blurb += thing.text[i]
          else:
            blurb = job_text
      print blurb + ' posted on ' + time_posted

main()
