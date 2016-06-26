import sys
import numpy as np

lines = open(sys.argv[1],'r').read().split('\n')
for li,line in enumerate(lines):
  if "Intelligence" in line:
    keep = lines[li+2]
    break
secs = keep.split("><")
hrefs = [sec for sec in secs if "href=" in sec]
links = set([href.split('"')[1] for href in hrefs])
with open("alllinks",'a') as outf:
  outf.write('\n'.join(links))
  outf.write('\n')
