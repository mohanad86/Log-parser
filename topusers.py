import os
import urllib
import gzip
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files
root = "/home/malyhass/logs"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
users = {}
total = 0
for filename in os.listdir(root):
	if not filename.startswith("access.log"):
		print "Skipping unknown file:", filename
		continue
	if filename.endswith(".gz"):
		fh = gzip.open(os.path.join(root, filename))
	else:
		fh = open(os.path.join(root, filename))    
	print "Going to process:", filename
	for line in fh:
		total = total + 1
		try:
			source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
			method, path, protocol = request.split(" ")
			unpath = urllib.unquote(path)
			if unpath.startswith("/~"):
				username, remainder = unpath[2:].split("/",1)
				#print "User found:", username
				try:
					users[username] = users[username] + 1
				except:
					users[username] = 1

			url = "http://enos.itcollege.ee" + unpath
			try:
				urls[url] = urls[url] + 1
			except:
				urls[url] = 1

			for keyword in keywords:
				if keyword in agent:
					try:
						d[keyword] = d[keyword] + 1
					except KeyError:
						d[keyword] = 1
					break # Stop searching for other keywords
		except ValueError:
			pass # This will do nothing, needed due to syntax
 
print "----------TOP 5 USERS----------"
print "Total lines:", total
userresult = users.items()
userresult.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in userresult[:5]:
	print keyword, "=", hits, "(", hits * 100 / total, "%)"
print "----------TOP 5 PAGES----------"
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
print "-------------------------------"
