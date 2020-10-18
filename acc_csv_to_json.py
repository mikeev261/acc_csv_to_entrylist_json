#!/usr/bin/python3
import pandas as pd
import sys, getopt
import json
#import csv
#USAGE: -i <inputfile.csv> -o <outputfile.json>

NAME = 2
STEAM_ID = 3

#def make_json_top():



def main(argv):
  input_csv = ''
  output_json = ''
  arguments = len(sys.argv) - 1
  if(arguments < 2):
    print ('USAGE: acc_csv_to_json.py -i <inputfile.csv> -o <outputfile.json>')
    sys.exit(2)  
  input_csv = sys.argv[1]
  output_json = sys.argv[2]
  print ('\nInput CSV: '+input_csv+'\n')
  print ('Output JSON: '+output_json+'\n')
  outfile = open(output_json, "w")
  
  df = pd.read_csv (input_csv)

  json_top = {}
  entries = {}
  teams = {}

  driver1 = {}
  #driver1['firstName'] = "Mike"
  driver1['firstName'] = df.iat[5,NAME].split(' ')[0]
  #driver1['lastName'] = "Evans"
  driver1['lastName'] = df.iat[5,NAME].split(' ')[1]
  driver1['shortName'] = (driver1['lastName'][0:3]).upper()
  driver1['driverCategory'] = 3
  driver1['playerID'] = "S76561197970355546"
  
  #driver2 = {}
  #driver2['firstName'] = "Cezar"
  #driver2['lastName'] = "Hernandez"
  #driver2['shortName'] = "CEZ"
  #driver2['driverCategory'] = 3
  #driver2['playerID'] = "S76561197970355547"

  #team['drivers'] = [driver1, driver2]
  teams['drivers'] = [driver1]

  teams['overrideDriverInfo'] = 0
  teams['isServerAdmin'] = 0
  entries = [teams]

  json_top['configVersion'] = 1
  json_top['entries'] = entries
  print(json.dumps(json_top), file=outfile)

  
  #df.to_json (output_json)
  #X = Row
  #Y = Col
  #print (df.iat[5,NAME])

  outfile.close()
  print ('Woo Done')

if __name__ == "__main__":
   main(sys.argv[1:])