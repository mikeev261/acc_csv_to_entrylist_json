#!/usr/bin/python3
#import pandas as pd
import sys, getopt
import json
import csv
#USAGE: -i <inputfile.csv> -o <outputfile.json>

#################
# ADJUSTMENTS
TOTAL_GT3 = 25
TOTAL_GT4 = 25
TOTAL_CAR_PER_TYPE = 4


#################


TEAM = 1
RACE_NUM = 2
FIRST = 3
LAST = 4
DISCORD_ID = 5
STEAM_ID = 6
LEAD_DRIVER = 7
CAR_1 = 8
CAR_2 = 9
CAR_3 = 10


#Preload total allocations
gt3_rem = TOTAL_GT3
gt4_rem = TOTAL_GT4

car_dict = {
    1: "Aston Martin V8 Vantage GT3",
    2: "Aston Martin V12 Vantage GT3",
    3: "Audi R8 LMS GT3",
    4: "Audi R8 LMS GT3 Evo",
    5: "Bentley Continental GT3",
    6: "BMW M6 GT3",
    7: "Ferrari GT3 (2018)",
    8: "Ferrari GT3 Evo (2020)",
    9: "Honda NSX GT3 (2018)",
    10: "Honda NSX GT3 Evo (2019)",
    11: "Jaaaaaaaaaaaaaaaaaaaaaaaaag GT3",
    12: "Lamborghini Huracan GT3 (2015)",
    13: "Lamborghini Huracan GT3 Evo (2019)",
    14: "Lexus RC F GT3",
    15: "McLaren 650S GT3",
    16: "McLaren 720S GT3",
    17: "Mercedes AMG GT3 (2015)",
    18: "Mercedes AMG GT3 Evo (2020)",
    19: "Nissan GT-R GT3 (2015)",
    20: "Nissan GT-R GT3 (2018)",
    21: "Porsche 991 GT3 R",
    22: "Porsche 991 II GT3 R",
    23: "Alpine A110 GT4",
    24: "Aston Martin V8 Vantage GT4",
    25: "Audi R8 LMS GT4",
    26: "BMW M4 GT4",
    27: "Chevrolet Camaro GT4.R",
    28: "Ginetta G55 GT4",
    29: "KTM X-Bow GT4",
    30: "Maserati Granturismo MC GT4",
    31: "McLaren 570S GT4",
    32: "Mercedes AMG GT4",
    33: "Porsche 718 Cayman GT4 Clubsport",
}


print ("-----------------------------------")
print ("ACC CSV to JSON Entrylist Converter")
print ("-----------------------------------")

#def make_json_top():
input_csv = ''
output_json = 'entrylist.json'
arguments = len(sys.argv) - 1
if(arguments < 1):
  print ('USAGE: acc_csv_to_json.py <inputfile.csv> <admin STEAM_ID (optional)>')
  sys.exit(2)  
input_csv = sys.argv[1]
try:
    admin_steam_id = sys.argv[2]
    print ('Admin declared as ' + admin_steam_id)
except:
    admin_steam_id = ""
    print ('INFO: No Admin ID Declared. If you want someone to have admin access, re-run with their S# as a 2nd argument.\n')

print ('\nINFO: Input CSV: '+input_csv+'\n')
print ('INFO: Output JSON: entrylist.json\n')


def read_csv_write_json(input_csv, json_file):
  outfile = open(output_json, "w")
  csv_rows = []
  with open(input_csv) as csv_file:
    next(csv_file) # skip header line
    reader = csv.reader(csv_file) #read the CSV file and store that as "reader"
    json_top = {} #Initialize the top layer of the JSON
    entries = [] #Initialize the top of entries (one below json_top)
    row_index = 0 #Initialize the row index

    for row in reader:
      teams = {}

      driver1 = {}
      driver1['firstName'] = row[FIRST]
      driver1['lastName'] = row[LAST]
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
      #print(row[EMAIL])
    json_top['configVersion'] = 1
    json_top['entries'] = entries
    json_top['forceEntryList'] = 1
    print(json.dumps(json_top), file=outfile)
    outfile.close()
    
    print ('-----------')
    print ('VROOM VROOM')

def convert_write_json(data, json_file):
  with open(json_file, "w") as f:
    f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
    f.write(json.dumps(data))


read_csv_write_json(input_csv, output_json)