import subprocess as sub

list_set = open("list_set",'r').read().split('\n')
list_set.pop()
list_set = [l.split() for l in list_set]
for li in list_set:
  addr = "http://www.dogbreedslist.info/%s/%s"%(li[0],li[1])
  print(sub.check_output("wget %s -O %s.%s"%(addr,li[0],li[1]),shell=True))
