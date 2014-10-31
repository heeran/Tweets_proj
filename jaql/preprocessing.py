#!/usr/bin/python
import sys
import re
import json
import getopt
import io

def parse_tweet_json(tweet, list_of_keys):
  parsed_tweet = json.loads(tweet)

  # a filtered tweet using a dictionary
  filtered_tweet = {}  
  for mykey in list_of_keys:
    search_key = mykey
    
     # simple keys
    myvalue = parsed_tweet.get(mykey)
    filtered_tweet[mykey] = myvalue
     # complex keys
     #search_key = mykey.split('__') 
     #filtered_tweet[mykey] = scan_dictionary(parsed_tweet, search_key)
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
     print sys.argv[0], "[input file] [output file]" 
     print ""
     print "Description:"
     print "Arguments:"
     print "input file -> a JSON file containing records (one per line)"
     print "output file -> a file to write the extracted key/value pairs of JSON records; one record per line"
     exit(1)
   
   # Create a list of key to extract from the tweets
   list_of_keys = []
   list_of_keys.append("contributors")
   list_of_keys.append("text")
   list_of_keys.append("geo")
   list_of_keys.append("retweeted")
   list_of_keys.append("in_reply_to_screen_name")
   list_of_keys.append("possibly_sensitive")
   list_of_keys.append("truncated")
   list_of_keys.append("lang")
   list_of_keys.append("entities")
   list_of_keys.append("in_reply_to_status_id_str")
   list_of_keys.append("id")
   list_of_keys.append("source")
   list_of_keys.append("in_reply_to_user_id_str")
   list_of_keys.append("retweet_count")
   list_of_keys.append("created_at")
   list_of_keys.append("in_reply_to_user_id")
   list_of_keys.append("id_str")
   list_of_keys.append("place")
   list_of_keys.append("text")
   list_of_keys.append("user")
   list_of_keys.append("coordinates")
   #for i in xrange(3, len(sys.argv)):
   #list_of_keys.append(sys.argv[i])
     
   # print list_of_keys
   parse_file(sys.argv[1], sys.argv[2], list_of_keys)
