import os
import urllib
import gzip
import argparse
import gzip
import GeoIP
gi = GeoIP.open("GeoIP.dat", GeoIP.GEOIP_MEMORY_CACHE)
parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path', help='Path to Apache2 log files', default="/home/malyhass/logs")
parser.add_argument('--top-urls', help="Find top URL-s", action='store_true')
parser.add_argument('--geoip', help ="Resolve IP-s to country codes", default="/home/malyhass/GeoIP.dat")
parser.add_argument('--verbose', help="Increase verbosity", action="store_true")
args = parser.parse_args()
#this is the directory where is the log files locate,
#root = "/home/malyhass" if you working on the server you can use it without the path
keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
total = 0
files = []
users = {}
countries = {}
ip_addresses = {}
user_bytes ={}
for filename in os.listdir(args.path):
    if not filename.startswith("access.log"):
        print "Skipping unknown file:", filename
        continue

    if filename.endswith(".gz"):
      continue
      fh = gzip.open(os.path.join(args.path, filename))
    else:
        fh = open(os.path.join(args.path, filename))
    if args.verbose:
        print "Parsing:", filename
    for line in fh:
        total = total + 1
        try:
            source_timestamp, request, response, referrer, _, agent, _ = line.split("\"")
            method, path, protocol = request.split(" ")
        except ValueError:
            continue # Skip garbage

        source_ip , _, _, timestamp = source_timestamp.split(" ", 3)
        
        if not ":" in source_ip: 
           ip_addresses[source_ip] = ip_addresses.get(source_ip, 0) + 1

           cc = gi.country_code_by_addr(source_ip)
           countries[cc] = countries.get(cc, 0) + 1
       
            
        
            
        if path == "*": continue # Skip asterisk for path

        _, status_code, content_length, _ = response.split(" ")
        content_length = int(content_length)
        path = urllib.unquote(path)
        
        if path.startswith("/~"):
            username = path[2:].split("/")[0]
            try:
               user_bytes[username] = user_bytes[username] + content_length
            except:
                user_bytes[username] = content_length

        try:
           urls[path] = urls[path] + 1
        except:
           urls[path] = 1
        
        for keyword in keywords:
            if keyword in agent:
               try:
                   d[keyword] = d[keyword] + 1
               except KeyError:
                    d[keyword] = 1
               break
if not urls:
    print("No log files!")
    exit(255)
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
from lxml import etree
from lxml.cssselect import CSSSelector
 
document =  etree.parse(open('BlankMap-World6.svg'))

max_hits = max(countries.values())
print("country with max amount of hits:", max_hits)
for country_code, hits in countries.items():
    if not country_code: continue
    print country_code, hex(hits * 255 / max_hits) [2:]
    sel = CSSSelector("#" + country_code.lower())
    for j in sel(document):
        j.set("style", "fill:#" + hex(hits * 255 / max_hits)[2:] + "0000")
        for i in j.iterfind("{http://www.w3.org/2000/svg}path"):
            i.attrib.pop("class", "")
 
with open("highlighted.svg", "w") as fh:
    fh.write(etree.tostring(document))
for filename in os.listdir("."):
    mode, inode, device, nlink, vid, gid, size, atime, mtime, ctime = os.stat(filename) 
    files.append((filename, datetime.fromtimestamp(mtime), size))
files.sort(key = lambda(filename, dt, size):dt)
print "Newest file is:", files[-1][0]
print "Oldesr file is:", files[0][0]
for filename, dt, size in files:
    print filename, dt, humanize(size)
print"************************"
print("Top IP-addresses:")
results = ip_addresses.items()
results.sort(key = lambda item:item[1], reverse=True)
for ip, hits in results[:5]:
    print ip, "==>", hits, "(", hits * 100 / total, "%)"
print "************************"
print "Total lines =", total
print "***********************"
result = urls.items()
result.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in result[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
print "************************"
