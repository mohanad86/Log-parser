import os
from threading import Thread
from PIL import Image
d = "/home/malyhass/log-parser/image"
output = os.path.join(d, "smaller")
filenames = os.listdir(d)
class ImageConverter(Thread):
    def run(self):
        while True:
            try :
                 filename = filenames.pop()
            except IndexError:
                break
            if not filename.lower().endswith("jpg"):
                continue
            print self.getName(), "is processing", filename    
            im = Image.open(os.path.join(d, filename))
            width, height = im.size
            smaller = im.resize((400, height * 800 / width))
            smaller.save(os.path.join(output, filename))

if not os.path.exists(output):
    os.makedirs(output)

threads = []
for i in range (0, 2):
    threads.append(ImageConverter())
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
   
