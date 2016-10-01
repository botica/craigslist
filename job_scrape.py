# scrapes craigslist's city of chicagos food bev and hosp jobs page
# prints out today's jobs
#
# todo:
# implement days ago instead of one day
# implement parsing the location, usingg outer element of class 'txt' not 'pl'
# implement searching from other craigslist locations and job types
#
# run as $python job_scrape.py <RADIUS> <ZIPCODE>
# with radius in miles and zipcode being a chicago zip code

import urllib
import time
from lxml.html import parse
import sys

class craigsCrawler:

  def __init__(self, radius, zipcode):
    self.url = 'https://chicago.craigslist.org/search/chc/fbh?sort=date&search_distance=' + str(radius) + '&postal=' + str(zipcode)
    self. blurb_limit = 60 # amount of text to print to console for each job title
    self.jobs = [] # to be popuated with jobs as they are parsed

  def parse_date(self, date_string):
    """takes a string as "YYYY-MM-DD 24:00" format and returns parsed"""
    split1 = date_string.split('-')
    year = split1[0]
    month = split1[1]
    split2 = split1[2].split(' ')
    day = split2[0]
    time = split2[1] # 24:00 format
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
    
  def get_time(self):
    t = 'AM'
    hours, minutes = self.time.split(':')
    h = int(hours)
    if h >= 12:
      t = 'PM'
    if h > 12:
      h -= 12
    hours = str(h)
    return hours   + ':' + minutes + ' ' + t


def get_page(url):
  """trys to download and parse an html doc with lxml"""
  try:
    print 'getting page'
    handle = urllib.urlopen(url)
    page = parse(handle).getroot()
    return page
  except IOError as e:
    print 'problem connecting'
    return None
  except UnicodeEncodeError:
    print 'format error'
    return None
  except UnicodeError:
    print 'format error'
    return None

def main():
  """downloads and parses a craigslist page for info about jobs"""
  if len(sys.argv) != 3:
    print 'run as $python job_scrape.py <MILE RADIUS> <ZIP CODE>'
    return
  radius = sys.argv[1]
  zipcode = sys.argv[2]
  c = craigsCrawler(radius, zipcode)
  html = get_page(c.url)# try to download and parse the html doc to lxml.html object tree
  if html != None:
    pls = html.find_class('pl') # inner most class row row posting with class name
    #pls.find_class('hdrlnk')
    #texty = html.find_class('txt')# inner class of class 'row' that contains title text and optional location
    #print txt[0][0][2].text # title text
    for pl in pls:
      for element in pl:
        if element.tag == 'time':
          date_posted = element.get('datetime')
          parsed_date = c.parse_date(date_posted)
        elif element.tag == 'a': # also looking for the job description title text
          job_text = element.text
      j = job(job_text, parsed_date[0], parsed_date[1], parsed_date[2], parsed_date[3],)# create a job instance
      c.add_job(j)# add it to the crawler
  today = time.strftime('%d')# prepare information for printing
  new_jobs = []
  for j in c.jobs:
    if j.get_day() == today:
      new_jobs.append(j)
  new_jobs.reverse()
  print 'jobs today:'# print out the jobs posted that day on the given page
  for j in new_jobs:
    print j.get_text()[:c.blurb_limit] + ' posted at ' + j.get_time()
  print ''
  print str(len(new_jobs)) + ' jobs posted today on ' + c.url
  print str(len(c.jobs)) + ' jobs scraped total on ' + c.url

main()

