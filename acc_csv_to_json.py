#!/usr/bin/python3
#import pandas as pd
import sys, getopt
import json
import csv
#USAGE: -i <inputfile.csv> -o <outputfile.json>

EMAIL = 1
NAME = 2
STEAM_ID = 3

#def make_json_top():
input_csv = ''
output_json = 'entrylist.json'
arguments = len(sys.argv) - 1
if(arguments < 1):
  print ('USAGE: acc_csv_to_json.py <inputfile.csv> <admin STEAM_ID (optional)>')
  sys.exit(2)  
input_csv = sys.argv[1]
admin_steam_id = sys.argv[2]
print ('\nInput CSV: '+input_csv+'\n')
print ('Output JSON: entrylist.json\n')


def read_csv_write_json(input_csv, json_file):
  outfile = open(output_json, "w")
  csv_rows = []
  with open(input_csv) as csv_file:
    next(csv_file) # skip header line
    reader = csv.reader(csv_file)
    json_top = {}
    entries = []
    row_index = 0

    for row in reader:
      teams = {}

      driver1 = {}
      driver1['firstName'] = row[NAME].split(' ')[0]
      num_names = len(row[NAME].split())
      if(num_names<2):
        driver1['lastName'] = row[NAME].split(' ')[0]
      else:
        driver1['lastName'] = row[NAME].split(' ')[1]
      driver1['shortName'] = (driver1['lastName'][0:3]).upper()
      driver1['driverCategory'] = 3
      driver1['playerID'] = "S"+row[STEAM_ID]
      
      teams['drivers'] = [driver1]

      teams['overrideDriverInfo'] = 0
      if(driver1['playerID']==admin_steam_id):
        teams['isServerAdmin'] = 1
      else:
        teams['isServerAdmin'] = 0
      entries.append(teams)


      row_index += 1
      print(row[EMAIL])
    json_top['configVersion'] = 1
    json_top['entries'] = entries
    json_top['forceEntryList'] = 1
    print(json.dumps(json_top), file=outfile)
    outfile.close()
    
    print ('VROOM VROOM')

def convert_write_json(data, json_file):
  with open(json_file, "w") as f:
    f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
    f.write(json.dumps(data))


read_csv_write_json(input_csv, output_json)