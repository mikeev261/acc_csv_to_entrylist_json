#!/usr/bin/python3
import pandas as pd
import sys, getopt
import json
import array
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
print ("-----------------------------------")
print ("ACC CSV to JSON Entrylist Converter")
print ("-----------------------------------")

print ("\n AVAILABLE CARS:\n")

car_dict = {
    0: "Porsche 991 GT3 R",
    1: "Mercedes AMG GT3 (2015)",
    2: "Ferrari 488 GT3 (2018)",
    3: "Audi R8 LMS GT3",
    4: "Lamborghini Huracan GT3 (2015)",
    5: "McLaren 650S GT3",
    6: "Nissan GT-R GT3 (2018)",
    7: "BMW M6 GT3",
    8: "Bentley Continental GT3 (2018)",
    9: "Porsche 991II GT3 Cup",
    10: "Nissan GT-R GT3 (2017)",
    11: "Bentley Continental GT3 (2016)",
    12: "Aston Martin V12 Vantage GT3",
    13: "Lamborghini Gallardo R-EX GT3",
    14: "Jaaaaaaaaaaaaaaaaaaaaaaaaag GT3",
    15: "Lexus RC F GT3",
    16: "Lamborghini Huracan GT3 Evo (2019)",
    17: "Honda NSX GT3 (2018)",
    18: "Lamborghini Huracan SuperTrofeo",
    19: "Audi R8 LMS GT3 Evo",
    20: "Aston Martin V8 Vantage GT3",
    21: "Honda NSX GT3 Evo (2019)",
    22: "McLaren 720S GT3",
    23: "Porsche 991 II GT3 R",
    24: "Ferrari 488 GT3 Evo (2020)",
    25: "Mercedes AMG GT3 Evo (2020)",
    26: "",
    27: "",
    28: "",
    29: "",
    30: "",
    31: "",
    32: "",
    33: "",
    34: "",
    35: "",
    36: "",
    37: "",
    38: "",
    39: "",
    41: "",
    42: "",
    43: "",
    44: "",
    45: "",
    46: "",
    47: "",
    48: "",
    49: "",
    50: "Alpine A110 GT4",
    51: "Aston Martin V8 Vantage GT4",
    52: "Audi R8 LMS GT4",
    53: "BMW M4 GT4",
    54: "",
    55: "Chevrolet Camaro GT4.R",
    56: "Ginetta G55 GT4",
    57: "KTM X-Bow GT4",
    58: "Maserati Granturismo MC GT4",
    59: "McLaren 570S GT4",
    60: "Mercedes AMG GT4",
    61: "Porsche 718 Cayman GT4 Clubsport",
}


car_rem = array.array('I') #Instantiate car_rem array (empty)

for car in car_dict:
    car_rem.append(TOTAL_CAR_PER_TYPE) #Initialize a new per-type value
    if(bool(car_dict[car])):
        print(car, ': ', car_dict[car])

#car_rem[5] -= 1;
#print(car_rem)


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
    print ('\nAdmin declared as ' + admin_steam_id)
except:
    admin_steam_id = ""
    print ('\nINFO: No Admin ID Declared. If you want someone to have admin access, re-run with their S# as a 2nd argument.\n')

print ('\nINFO: Input CSV: '+input_csv+'\n')
print ('INFO: Output JSON: entrylist.json\n')

def car_num_lookup(car_dict, car_name):
    for car in car_dict:
        if(car_dict[car] == car_name):
            return car

def read_csv_write_json(input_csv, json_file, lead):
  outfile = open(output_json, "r+") #Re-open as r/w
  #outfile.seek(0) #Rewind
  csv_rows = []
  with open(input_csv) as csv_file:
    next(csv_file) # skip header line
    reader = csv.reader(csv_file) #read the CSV file and store that as "reader"

    if(lead):
        json_top = {} #Initialize the top layer of the JSON
        entries = [] #Initialize the top of entries (one below json_top)

    for row in reader:
        driver = {} #Always initialize this for every pass
        if(lead): #First pass
            team = {}
            if(row[LEAD_DRIVER] == "No"): #Not the lead driver, skip for this pass
                continue #Skip iteration of this loop
        else: #not lead
            if(row[LEAD_DRIVER] == "Yes"): #Lead driver, skip for this pass (we got them already)
                continue #Skip iteration of this loop

        driver['firstName'] = row[FIRST]
        driver['lastName'] = row[LAST]
        driver['shortName'] = (driver['lastName'][0:3]).upper()
        driver['driverCategory'] = 3
        driver['playerID'] = "S"+row[STEAM_ID]
    
        
        if(lead): #Team info
            team['drivers'] = [driver]
            team['overrideDriverInfo'] = 1
        
            if(driver['playerID']==admin_steam_id):
                team['isServerAdmin'] = 1
            else:
                team['isServerAdmin'] = 0
            
            team['forcedCarModel'] = car_num_lookup(car_dict, row[CAR_1])
            team['raceNumber'] = int(row[RACE_NUM])
            entries.append(team)



        #if(not lead): #We are now iterating through the JSON to add the teammates
        #    for entries in outfile
        #    drivers.append(driver)


        #print(row[EMAIL])
    if(lead): #Team info
        json_top['configVersion'] = 1
        json_top['entries'] = entries
        json_top['forceEntryList'] = 1
        print(json.dumps(json_top, indent=4), file=outfile)
    outfile.close()

    


#def convert_write_json(data, json_file):
#  with open(json_file, "w") as f:
#    f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
#    f.write(json.dumps(data))


#Open the JSON output file
outfile = open(output_json, "w")

#First, form teams by applying lead drivers ONLY
read_csv_write_json(input_csv, outfile, 1)


#Next, populate teams with teammates
read_csv_write_json(input_csv, outfile, 0)

print ('-----------')
print ('VROOM VROOM')
#Close the JSON outfile
