#!/usr/bin/python
import sys
import re
import json
import getopt

def parse_tweet_json(tweet, list_of_keys):
  parsed_tweet = json.loads(tweet)

  # a filtered tweet using a dictionary
  filtered_tweet = {}  
  for mykey in list_of_keys:
    search_key = mykey.split('__')

    # simple keys
    #myvalue = parsed_tweet.get(mykey)
    #filtered_tweet[mykey] = myvalue

    # complex keys
    filtered_tweet[mykey] = scan_dictionary(parsed_tweet, search_key)
  return filtered_tweet

def scan_dictionary(my_dict, search_key):
  try:
    result = reduce(dict.__getitem__, search_key, my_dict)
  except (KeyError, TypeError):
    pass
  else:
    return result

def delete_lastline_comma(filename):
  with open(filename,"r+") as myfile:
   lines = myfile.readlines()
   myfile.writelines([item for item in lines[:-1]]) #delete last line 
   myfile.writelines("]")
   myfile.close()

def parse_file(filename, output, list_of_keys):
  with open(filename, "r") as myfile, open(output, "wb") as myout:
    myout.write("[")
    for line in myfile:
      filtered_tweet = parse_tweet_json(line, list_of_keys)
      json.dump(filtered_tweet, myout)
      myout.write("\n,")
    myout.write("]")
  myout.close()
  delete_lastline_comma(output)

if __name__ == "__main__":
   if len(sys.argv) < 3:
     print sys.argv[0], "[input file] [output file] [key1] [key2] ..." 
     print ""
     print "Description:"
     print "Using this program, you can extract  keys (and their values) from a collection of JSON records." 
     print "Thus, you can flatten the nested structure of JSON records."
     print ""
     print "Arguments:"
     print "input file -> a JSON file containing records (one per line)"
     print "output file -> a file to write the extracted key/value pairs of JSON records; one record per line"
     print "key* -> a key in a JSON record; if nesting is needed use colon as a delimiter; e.g., user:followers_count"
     exit(1)
   # Create a list of key to extract from the tweets
   list_of_keys = []
   for i in xrange(3, len(sys.argv)):
     list_of_keys.append(sys.argv[i])
   # print list_of_keys
   parse_file(sys.argv[1], sys.argv[2], list_of_keys)
