import os
import urllib
import gzip
import argparse
import gzip
parser = argparse.ArgumentParser(description='Apache2 log parser.')
parser.add_argument('--path', help='Path to Apache2 log files', default="/home/malyhass/Documents")
parser.add_argument('--top-urls', help="Find top URL-s", action='store_true')
parser.add_argument('--geoip', help ="Resolve IP-s to country codes", action='store_true')
parser.add_argument('--verbosity', help="Increase verbosity", action="store_true")
args = parser.parse_args()
#this is the directory where is the log files locate,
root = "/home/mohanad"

keywords = "Windows", "Linux", "OS X", "Ubuntu", "Googlebot", "bingbot", "Android", "YandexBot", "facebookexternalhit"
d = {} 
urls = {}
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
             url = "http://enos.itcollege.ee" + urllib.unquote(path)
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

print "Top 5 USERS", total
print "***********************"
print "Total lines:", total
print "***********************"
print "TOP 5 PAGES", total
result = urls.items()
result.sort(key = lambda item:item[1], reverse=True)
for keyword, hits in result[:5]:
    print keyword, "==>", hits, "(", hits * 100 / total, "%)"
