# scrapes craigslist's city of chicagos food bev and hosp jobs page for lastest 100 postings
# implement radius, zip code, and as cmd args

import urllib
import time
from lxml.html import parse

class craigsCrawler:

  def __init__(self):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date'
    self. blurb_limit = 60 # amount of text to print to console
    self.jobs = [] # to be popuated with jobs

  def parse_date(self, date_string):
    split1 = date_string.split('-')
    year = split1[0]
    month = split1[1]
    split2 = split1[2]
    split2 = split2.split(' ')
    day = split2[0]
    time = split2[1] # 24:00
    return [day, month, year, time]

  def add_job(self, job):
     self.jobs.append(job)


class job:

  def __init__(self, text, day, month, year, time):
    self.text = text
    self.day = day
    self.month = month
    self.year = year
    self.time = time

  def get_text(self):
    return self.text

  def get_day(self):
    return self.day


#function to get and parse html
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
  today = time.strftime('%d') # this day
  jobs_today = 0
  html = get_page(c.url)
  if html != None:
    pls = html.find_class('pl') # inner most class row row posting with class name
    for pl in pls:
      for thing in pl:
        if thing.tag == 'time': # looking for tag -time- with attr -datetime- 
          date_posted = thing.get('datetime') # use get which takes attr and returns the value
          parsed_date = c.parse_date(date_posted) # that day
          if parsed_date[0] == today: # if same as today
            jobs_today += 1 # it was posted today
        elif thing.tag == 'a': # also looking for the job description title text
          job_text = thing.text 
          blurb = job_text[:c.blurb_limit] # crop it to the blurb limit
      j = job(job_text, parsed_date[0], parsed_date[1], parsed_date[2], parsed_date[3],)
      c.add_job(j)
      #print blurb + ' posted on ' + date_posted
  print str(jobs_today) + ' new jobs posted today on fbh:'
  #print str(len(c.jobs)) + ' jobs scraped total'
  for j in c.jobs:
    if j.get_day() == today:
      print j.get_text()[:c.blurb_limit]

main()

