"""
soUPerfind 0.1
UPCAT Results Search Engine
(c) Kix Panganiban 2011
Requires:
Python 2.7 and BeautifulSoup 4.0
"""

from bs4 import BeautifulSoup
import httplib
import re
import threading

"""
The main crawler thread class.
"""
class crawler(threading.Thread):
	# Running crawlers counter
	running = 0

	def __init__(self, cid, resultset, totalEntries, totalResults):
		self._id = cid
		self._resultset = resultset 
		self._entries = totalEntries
		self._results = totalResults
		self._links = []
		threading.Thread.__init__(self)

	# Adds a link to crawl in crawler queue
	def addLink(self,link):
		self._links.append(link)

	def run(self):
		for link in self._links:
			try:
				self._crawlConn = httplib.HTTPConnection('upcat.up.edu.ph')
				self._crawlConn.request('GET', '/results/'+link)
				self._pageRes = self._crawlConn.getresponse()
			except:
				print "Error retrieving results at: http://upcat.up.edu.ph/results/"+link
			self._pageData = self._pageRes.read()
			self._pageSoup = BeautifulSoup(self._pageData)
			
			# Parse and store data
			tableItem = self._pageSoup.find("table", class_='printable')
			tdItem = tableItem.find_all("td", class_='printable')
			itemType = 0
			# initialize current student array
			currStudent = [" ", " ", " ", " "]	
			for itemContent in tdItem:
				currStudent[itemType] = itemContent.get_text()
				if itemType == 3:
					itemType = 0
					# if query is found in any of the four fields
					if (re.search(query, currStudent[0], re.IGNORECASE)) or (re.search(query, currStudent[1], re.IGNORECASE)) or (re.search(query, currStudent[2], re.IGNORECASE)) or (re.search(query, currStudent[3], re.IGNORECASE)):
						print "\nMatch: \n" + currStudent[0] + "\n" + currStudent[1] + "\n" + currStudent[2] + "\n" + currStudent[3]
						self._resultset.append([currStudent[0], currStudent[1], currStudent[2], currStudent[3]])
						self._results += 1
					self._entries += 1
				else:
					itemType += 1
			print "Crawler #" +str(self._id) + ": http://upcat.up.edu.ph/results/"+link+" done."

		crawler.running -= 1
		print "Crawler #" + str(self._id) + " done! ("+str(crawler.running)+" crawlers left.)"


"""
Main execution line.
"""
print "-------------------------------"
print "soUPerfind: UPCAT Search Engine" 
print "using Python and BeautifulSoup"
print "-------------------------------"
print "Connecting...",
# Connect to UPCAT results server
try:
	mainConn = httplib.HTTPConnection('upcat.up.edu.ph')
	mainConn.request('GET', '/results/')
	mainRes = mainConn.getresponse()
except:
	print "Error connecting to UPCAT server."
	exit()
mainData = mainRes.read()
print " OK"

# Invokes BeautifulSoup on UPCAT mainpage
mainSoup = BeautifulSoup(mainData)

print "Locating listing pages...",
# Mainpage link array
mainLinks = []
for link in mainSoup.find_all('a'):
	if 'page' in link.get('href'):
		mainLinks.append(link.get('href'))
print " OK"
query = raw_input("Enter search query: ")
query.upper()
print "\nSearching (10 active crawlers)..."

# Initialize results storage
resultSet = []
results = 0
entries = 0

# Crawler array
crawlers = []
crawlerId = 0

# Initialize crawlers
for i in range(0,10):
	newCrawler = crawler(i, resultSet, entries, results)
	crawlers.append(newCrawler)

# Set crawlers free!
for link in mainLinks:
	crawlers[crawlerId].addLink(link)

	if not crawlers[crawlerId].isAlive():
		crawlers[crawlerId].start()
		print "Crawler #" + str(crawlerId) + " started!"
		crawler.running += 1
	
	if crawlerId == 9:
		crawlerId = 0
	else:
		crawlerId += 1

while(True):
	if crawler.running == 0:
		print "Done. " + str(entries) + " entries searched; " + str(results) + " matches."
		break
