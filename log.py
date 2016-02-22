import gzip
# gzip.open will give you a file object which transparently uncompresses the file as it's read
for line in gzip.open("/var/log/apache2/access.log.1.gz"):
    print line
