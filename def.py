import argparse

parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path', help='Path to Apache2 log files', default="/home/malyhass/Documents")
parser.add_argument('--top-urls', help="Find top URL-s", action='store_true')
parser.add_argument('--geoip', help ="Resolve IP-s to country codes", action='store_true')
parser.add_argument('--verbosity', help="Increase verbosity", action="store_true")
args = parser.parse_args()


import os
import urllib
import gzip
# Following is the directory with log files,
# On Windows substitute it where you downloaded the files

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
users = {}
total = 0
for filename in os.listdir(args.path):
	if not filename.startswith("access.log"):
		print "Skipping unknown file:", filename
		continue
	if filename.endswith(".gz"):
		fh = gzip.open(os.path.join(args.path, filename))
	else:
		fh = open(os.path.join(args.path, filename))    
	print "Going to process:", filename
	for line in fh:
		total = total + 1
		try:
			source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
			method, path, protocol = request.split(" ")
			path = urllib.unquote(path)
			if path.startswith("/~"):
				username, remainder = path[2:].split("/",1)
				#print "User found:", username
				try:
					users[username] = users[username] + 1
				except:
					users[username] = 1

			url = "http://enos.itcollege.ee" + path
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
			
def humanize(bytes):
    if bytes < 1024:
        return "%d B" % bytes
    elif bytes < 1024 ** 2:
        return "%.1f KB" % (bytes / 1024.0)
    elif bytes < 1024 ** 3:
        return "%.1f MB" % (bytes / 1024.0 ** 2)
    else:
        return "%.1f GB" % (bytes / 1024.0 ** 3)
for filename in os.listdir("."):
    mode, inode, device, nlink, vid, gid, size, atime, mtime, ctime = os.stat(filename) 
    print filename, humanize(size) 
 
print "TOP 5 USERs"
print "Total lines:", total
results = users.items()
results.sort(key = lambda item:item[1], reverse=True)
for user, transferred_bytes in results[:5]:
    print user, "==>", humanize(transferred_bytes)
print "TOP 5 PAGES"
results = urls.items()
results.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in results[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
