#!/usr/bin/python

import json, sys, getopt, os, csv
from collections import Counter

def usage():
  print("Usage: %s --file=[filename]" % sys.argv[0])
  sys.exit()

def main(argv):

  file=''
 
  myopts, args = getopt.getopt(sys.argv[1:], "", ["file="])
 
  for o, a in myopts:
    if o in ('-f, --file'):
      file=a
    else:
      usage()

  if len(file) == 0:
    usage()
 
  corpus = open(file)
  urldata = json.load(corpus, encoding="latin1")
  
  #Count malicious urls in train.JSON
  # print("Malicious url:")
  # print(sum(1 for record in urldata if record['malicious_url'] == 1))
  # print ("Clean url:")
  # print(sum(1 for record in urldata if record['malicious_url'] == 0))

  #Count total num of urls in both files.
  #print(sum(1 for record in urldata))

    # Do something with the URL record data...
  
  for record in urldata:
        point = 0
        if record["malicious_url"]== 1:
              point += 5

        if record["domain_age_days"]>700:
              point += 5
        elif record["domain_age_days"]<700:
              point -= 2
      
        if record["alexa_rank"] == "null" or record["alexa_rank"] > 1000000:
              point += 3
        elif record ["alexa_rank"]< 1000000:
              point -= 3

        if record["query"] == "null":
              point += 2
        else:
              point -= 1
        
        if record["ips"] is None:
              point += 2
        
        if record["file_extension"] != "null":
              point += 3
        else:
              point -= 1
        
        if record["num_path_tokens"] > 7:
              point += 1
        elif record["num_path_tokens"] < 7:
              point -= 1
        if record ["port"] not in (80,443):
              point += 1
       
        if point > 2:
              rate = record["url"]
              print (rate)
              print "Number of points:",point
              
  
  corpus.close()
  

if __name__ == "__main__":
  main(sys.argv[1:])
