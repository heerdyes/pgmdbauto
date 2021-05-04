#!/usr/bin/env python
from webbot import Browser
import time
import sys
import os
import shutil
import random
import zipfile
from config import *

# CLI args usage #
if len(sys.argv)!=4:
  print('[usage] python pgmdbfind.py RSNs.txt <vsmin> <vsmax>')
  raise SystemExit

# ---------------------------- function definitions -------------------------- #
# random string generator
def rndstr(n):
  s=''
  for i in range(n):
    s+=chr(random.randint(65,90))
  return s

# delay utility
def delay(ns,msg='activity'):
  print('[delay][%s] seconds: %s'%(msg,ns))
  time.sleep(ns)

# log in to peernga site
def sitelogin(web,url,uid,pwd):
  print('[sitelogin] url: %s'%url)
  web.go_to(url)
  print('[sitelogin] logging in')
  web.type(uid,into='Email',id='user_email')
  web.type(pwd,into='Password',id='user_password')
  web.click('Sign in')

# navigate to the search page
def navsearchpage(web,pageloc):
  print('[navsearchpage] url: %s'%pageloc)
  web.go_to(pageloc)
  print('[navsearchpage] proceed')
  web.click('Submit')
  
# click on the Download Time Series Records button
def downloadTSR(web,rsn,rsnselector,downloadTSR_selector,srchrec_selector):
  rsnstr=str(rsn)
  print('[downloadTSR][%s] populating RSN: %s into field %s'%(rsnstr,rsn,rsnselector))
  web.type(rsn,css_selector=rsnselector)
  print('[downloadTSR][%s] clicking on Search Records'%rsnstr)
  web.click(css_selector=srchrec_selector)
  delay(5,'search_results_populating')
  print('[downloadTSR][%s] clicking on Download TSR button'%rsnstr)
  web.click(css_selector=downloadTSR_selector)
  delay(0.3)
  web.driver.switch_to.alert.accept()
  delay(0.3)
  web.driver.switch_to.alert.accept()

# rename and move the file to desired location
def processresults(rsn,ssn,vsmax,vsmin):
  oldfile=os.path.join(DOWNLOADS_DIR,DEFAULT_DL_FILENAME)
  newfilename='%s_%s_%s-%s'%(str(rsn),ssn,vsmin,vsmax)
  print('[processresults] newfilename: %s'%newfilename)
  extn='.zip'
  newfile=os.path.join(TARGET_DIR,newfilename+extn)
  if os.path.isfile(newfile):
    print('[processresults][ERROR] target file %s already exists, doing nothing'%newfile)
    return
  if os.path.isfile(oldfile):
    print('[processresults] moving %s -> %s'%(oldfile,newfile))
    shutil.move(oldfile,newfile)
    xdir=os.path.join(UNZIP_DIR,newfilename)
    if os.path.isdir(xdir):
      print('[processresults] directory already exists: %s'%xdir)
      print('[processresults] going to ignore')
    else:
      with zipfile.ZipFile(newfile, 'r') as zf:
        print('[processresults] extracting to dir: %s'%xdir)
        zf.extractall(xdir)
  else:
    print('[processresults][ERROR] maybe file is not downloaded yet or wrong file name')

# make the downloads directory safe to download new peernga file
def predownloadchecks():
  oldfile=os.path.join(DOWNLOADS_DIR,DEFAULT_DL_FILENAME)
  futurefile=os.path.join(TARGET_DIR,str(rsn)+'.zip')
  if os.path.isfile(oldfile):
    print('[predownloadchecks][WARNING] seems like there is already a downloaded peernga file')
    backupfile=os.path.join(TARGET_DIR,'backup_%s_%s'%(rndstr(4),DEFAULT_DL_FILENAME))
    print('[predownloadchecks][WARNING]   backing it up to %s'%backupfile)
    os.rename(oldfile,backupfile)
  if os.path.isfile(futurefile):
    print('[predownloadchecks][WARNING] looks like there is already a file -> %s'%futurefile)
    return False
  return True


# --------------------- end of function definitions ------------------------ #

# script variables #
infilename=sys.argv[1]
vsmin=sys.argv[2]
vsmax=sys.argv[3]
web=Browser()

# process #
sitelogin(web,LOGIN_URL,UID,PWD)
navsearchpage(web,NGAWEST2_URL)
delay(1,'search_params_loading')
# for each RSN in input file
with open(infilename) as fin:
  rsnlines=fin.readlines()
  for srsn in rsnlines:
    rawline=srsn.rstrip()
    if len(rawline)==0:
      continue
    if rawline.startswith('#') or rawline.startswith('//'):
      continue
    parts=rawline.split(',')
    rsn,ssn,vs30=parts[0],parts[1],parts[2]
    print('[%s] rsn=%s'%(infilename,rsn))
    if not predownloadchecks():
      continue
    downloadTSR(web,rsn,RSN_SELECTOR,DOWNLOADTSR_SELECTOR,SEARCHRECORDS_SELECTOR)
    # hard coded to 3s for prototype purposes
    # consider dynamic polling to allow for large files
    delay(5,'downloading_search_results')
    processresults(rsn,ssn,vsmin,vsmax)

