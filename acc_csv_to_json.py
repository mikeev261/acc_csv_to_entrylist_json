#!/usr/bin/python3
import pandas as pd
import sys, getopt
import json
import array
import csv
import code
#USAGE: -i <inputfile.csv> -o <outputfile.json>

#################
# ADJUSTMENTS
TOTAL_GT3 = 50
TOTAL_GT4 = 0
TOTAL_CAR_PER_TYPE = 3


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
num_lead = 0 # num of lead drivers
num_team = 0 # num of team drivers
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
    10: "Nissan GT-R GT3 (2015)",
    11: "Bentley Continental GT3 (2015)",
    12: "Aston Martin V12 Vantage GT3",
    13: "Lamborghini Gallardo R-EX GT3",
    14: "Jaaaaaaaaaaaaaaaaaaaaaaaaag GT3",
    15: "Lexus RC F GT3",
    16: "Lamborghini Huracan GT3 Evo (2019)",
    17: "Honda NSX GT3 (2017)",
    18: "Lamborghini Huracan SuperTrofeo",
    19: "Audi R8 LMS GT3 Evo",
    20: "Aston Martin V8 Vantage GT3",
    21: "Honda NSX GT3 Evo (2019)",
    22: "McLaren 720S GT3",
    23: "Porsche 991 II GT3 R",
    24: "Ferrari GT3 Evo (2020)",
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
    sys.exit("ERROR: CAR NOT FOUND. Tried a car named: " + car_name)

def check_car(driver, car, num):
    global gt3_rem
    global gt4_rem
    if(car_rem[car] == 0):
        print("INFO: for ", driver, " try ", num, " no cars remaining of ", car)
        return False
    else: 
        if(car < 50): #GT3
            if(gt3_rem == 0):
                print("INFO: for ", driver, " try ", num, " no GT3 remaining.")
                return False
            else:
                return True
        else: #GT4
            if(gt4_rem == 0):
                print("INFO: for ", driver, " try ",  num, " no GT4 remaining.")
                return False
            else: 
                return True

def select_car(driver, car1, car2, car3):
    if(check_car(driver, car1, 1)):
        return car1
    elif(check_car(driver, car2, 2)):
        return car2
    elif(check_car(driver, car3, 3)):
        return car3
    else:
        print("ERROR: Driver " + driver + " had no valid cars selected!")
        print("ERROR: CAR1 = ", car1)
        print("ERROR: CAR2 = ", car2)
        print("ERROR: CAR3 = ", car3)
        sys.exit()




def read_csv_write_json(input_csv, lead):
    global gt3_rem
    global gt4_rem
    global num_lead
    global num_team

    csv_rows = []
    with open(input_csv) as csv_file:
        next(csv_file) # skip header line
        reader = csv.reader(csv_file) #read the CSV file and store that as "reader"
    
        if(lead):
            entries = [] #Initialize the top of entries (one below top_dict)
            num_lead = 0
        else: 
            num_team = 0
    
        for row in reader:
            gt3 = False
            driver = {} #Always initialize this for every pass
            if(lead): #First pass
                #Figure out if the car selection is legal
                car_num1 = car_num_lookup(car_dict, row[CAR_1])
                car_num2 = car_num_lookup(car_dict, row[CAR_2])
                car_num3 = car_num_lookup(car_dict, row[CAR_3])
                drivername = str(row[FIRST] + row[LAST])
                car_num = select_car(drivername, car_num1, car_num2, car_num3)
                gt3 = car_num < 50
                if(gt3):
                    gt3_rem -= 1
                else: 
                    gt4_rem -= 1
                team = {}
                if(row[LEAD_DRIVER] == "No"): #Not the lead driver, skip for this pass
                    continue #Skip iteration of this loop
            else: #not lead
                if(row[LEAD_DRIVER] == "Yes"): #Lead driver, skip for this pass (we got them already)
                    continue #Skip iteration of this loop
    
            driver['firstName'] = row[FIRST]
            driver['lastName'] = row[LAST]
            driver['shortName'] = (driver['lastName'][0:3]).upper()
            if(lead):
                if(gt3):
                    driver['driverCategory'] = 3
                else: #GT4
                    driver['driverCategory'] = 2
            driver_steam_id_filtered = filter(str.isdigit, row[STEAM_ID])
            driver_steam_id = "".join(driver_steam_id_filtered)
            driver['playerID'] = "S" + driver_steam_id 
    
            race_num_filtered = filter(str.isdigit, row[RACE_NUM])
            race_num = "".join(race_num_filtered)    
            
            if(lead): #Team info
                team['drivers'] = [driver]
                team['overrideDriverInfo'] = 1
            
                if(driver['playerID']==admin_steam_id):
                    team['isServerAdmin'] = 1
                else:
                    team['isServerAdmin'] = 0
                
                team['forcedCarModel'] = car_num
    
                team['raceNumber'] = int(race_num)
                entries.append(team)
                num_lead += 1
    
            if(not lead): #We are now iterating through the dict to add the teammates
                #num_team = 0
                for key in top_dict:
                    if(key == "entries"):
                        for i in range(len(top_dict[key])): #This is a list of dicts (each driver's form entry, prev a csv row)
                            team_race_number = int(top_dict[key][i]['raceNumber']) #Grab the dict entry race num for comparison
                            for key2 in top_dict[key][i]: #Now iterate through this driver's KEYS
                                #if(key2 == "drivers"): print("KEY2: ", key2, " race_num: ", race_num, "team_race_number: ", team_race_number)
                                if(key2 == "drivers" and int(race_num) == int(team_race_number)): #Compare the lead driver's race num with this driver
                                    #print("IN KEY2")
                                    driver['driverCategory'] = top_dict[key][i][key2][0]['driverCategory'] #Adopt the lead driver's category
                                    top_dict[key][i][key2].append(driver) #Append this driver to the lead driver's team list
                                    num_team +=1
        if(lead): #Team info
            top_dict['configVersion'] = 1
            top_dict['entries'] = entries
            top_dict['forceEntryList'] = 1
    if(lead): 
        print("# of Lead Drivers: ", num_lead)
    else: 
        print("# of Teammates: ", num_team)
        total_drv = num_team + num_lead
        print("Total number of drivers: ", total_drv)

#Open the JSON output file
outfile = open(output_json, "w")
top_dict = {} #Initialize the top dict

#First, form teams by applying lead drivers ONLY
read_csv_write_json(input_csv, 1)

#code.interact(local=locals()) #Jump into interactive mode

#Next, populate teams with teammates
read_csv_write_json(input_csv, 0)


print(json.dumps(top_dict, indent=4), file=outfile) #Print our dictionary out to JSON
outfile.close() #Close the JSON file

print("GT3's remaining: ", gt3_rem)
print("GT4's remaining: ", gt4_rem)
#print ("Number of Lead Drivers: ", num_lead)
#print ("Number of Teammate Drivers: ", num_team)
final_gt3 = int(TOTAL_GT3) - int(gt3_rem)
final_gt4 = TOTAL_GT4 - gt4_rem
print ("GT3 Cars: ", final_gt3)
print ("GT4 Cars: ", final_gt4)
print ('DONE!')
#Close the JSON outfile