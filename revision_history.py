import json
import urllib
import time
import re


#for extracting expressions for subject, predicate, object from the html text
pattern = '/m/[a-z0-9_]*'
pattern_pred = '/[a-z0-9_/]*'




from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

browser  = webdriver.Chrome()

api_key ='AIzaSyCj0ZvxQbOOoQPOB8EYb-3GeLCxlZLEL7o'

print "Enter the MID of the Freebase topic whose Revision History is required:  "
mid = raw_input()
print "Enter the name of the Freebase topic: "
name = raw_input()

service_url = 'https://www.freebase.com' + mid  + '?links&lang=en&historical=true'
browser.get(service_url)

time.sleep(1)

elem = browser.find_element_by_tag_name("body")

#to dynamically load all the content of the table
no_of_pagedowns = 100
while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

html = browser.page_source
soup = BeautifulSoup(html)

s = ""

cnt = 0

filename = 'RevisionHistoryOf_'+name+'.csv'

f = open(filename,'w')

#all the required content in td tags
for tag in soup.find_all('td'):
	t = tag.text
	t = t.strip()
	t = t.strip(' ')
	t = t.strip('\t')
	t = t.lstrip()
	tl = t.split('\n')
	t = ""

	for st in tl:
		if st == "Revert links":
			ss = ""
		elif st == "Filter by property":
			ss = ""
		elif st == "Filter by attribution":
			ss = ""
		elif st == "View property links":
			ss = ""
		elif st == "View property schema":
			ss = ""
		elif st == "View attribution links":
			ss = ""
		else:
			t = t + ' ' +  st
	t = t.lstrip()
	t = t.strip()	
	
	if cnt == 0:
		s = t
		cnt = cnt + 1
	elif cnt == 1: #extracting the subject mid
		match = re.search(pattern,t)
		if match:
			t = match.group()
			s = s + ',' +  t
			cnt = cnt + 1
	elif cnt == 2: #extracting the predicate
		match = re.search(pattern_pred,t)
		if match:
			t = match.group()
			s = s + ',' +  t
			cnt = cnt + 1
	else:
		if(cnt < 4 or cnt > 5):
			s = s + ',' +  t
			cnt = cnt + 1
		else:
			match = re.search(pattern_pred,t) #extracting the user id
			if match:
				t = match.group()
				s = s + ',' +  t
				cnt = cnt + 1
			match = re.search("none",t)
			if match:
				t = match.group()
				s = s + ',' +  t
				cnt = cnt + 1

	if(t == "insert" or t == "delete" or t == "update"): #last column values
		s = s.lstrip()
		s = s.strip() 
		f.write(s.encode('utf-8'))
		f.write('\n')
		print s
		cnt = 0
		s = ""

