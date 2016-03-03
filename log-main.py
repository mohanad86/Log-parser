import os
import urllib
import gzip
import argparse
import gzip
parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path', help='Path to Apache2 log files', default="/home/malyhass/logs")
parser.add_argument('--top-urls', help="Find top URL-s", action='store_true')
parser.add_argument('--geoip', help ="Resolve IP-s to country codes", action='store_true')
parser.add_argument('--verbosity', help="Increase verbosity", action="store_true")
args = parser.parse_args()
#this is the directory where is the log files locate,
root = "/home/malyhass"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
total = 0
files = []
ip_addresses = {}
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
            url = "http://enos.itcollege.ee" + urllib.unquote(path)
            source_ip,_,_, timestamp = source_timestamp.split(" ", 3)
           # print "Request came from:", source_ip, "When:", timestamp
            if not ":" in source_ip:
                ip_addresses[source_ip] = ip_addresses.get(source_ip, 0) + 1
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
                    break 

        except ValueError:
            pass 
from datetime import datetime
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
    files.append((filename, datetime.fromtimestamp(mtime), size))
files.sort(key = lambda(filename, dt, size):dt)
print "Newest file is:", files[-1][0]
print "Oldesr file is:", files[0][0]
for filename, dt, size in files:
	print "*********************"
    	print filename, dt, humanize(size)
print"************************"
print("Top IP-addresses:")
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for ip, hits in results[:5]:
    print ip, "==>", hits, "(", hits * 100 / total, "%)"
print "***********************"
print "Top 5 USERS =", total
print "***********************"
print "Total lines =", total
print "***********************"
print "TOP 5 URL =", total
result = urls.items()
result.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in result[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
