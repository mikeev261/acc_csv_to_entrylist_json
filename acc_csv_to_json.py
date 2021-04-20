#!/usr/bin/python3
import pandas as pd
import sys, getopt
import json
import array
import csv
import code
import yaml
from flatten_dict import flatten 
from flatten_dict import unflatten 
from datetime import datetime
#USAGE: -i <inputfile.csv> -o <outputfile.json>


yaml_path = "./CONFIG.yaml"


f_errors = open("ERROR.log", "+w")
f_log = open("RUN.log", "+w")
ERROR_BUF = ""
NUM_ERRORS = 0

def log(message):
    f_log.write(message)
    print(message)



try:
    log("Importing " + yaml_path)
    stream_yaml = open(yaml_path, "r")
except Exception as e:
    log(e)
    exit()

log("CONFIG.yaml Settings:")
settings = yaml.full_load(stream_yaml)
for node, node_settings in settings.items():
    log(node + ": " + str(node_settings) + "\n") 



#code.interact(local=locals()) #Jump into interactive mode

#################
# ADJUSTMENTS
TOTAL_GT3 = settings['car_limits']['total_gt3']
TOTAL_GT4 = settings['car_limits']['total_gt4']
TOTAL_CAR_PER_TYPE = settings['car_limits']['total_car_per_type']
#################


TEAM = settings['google_form_alignment']['team']
RACE_NUM = settings['google_form_alignment']['race_num']
FIRST = settings['google_form_alignment']['first']
LAST = settings['google_form_alignment']['last']
DISCORD_ID = settings['google_form_alignment']['discord_id']
STEAM_ID = settings['google_form_alignment']['steam_id']
LEAD_DRIVER = settings['google_form_alignment']['lead_driver']
CAR_1 = settings['google_form_alignment']['car_1']
CAR_2 = settings['google_form_alignment']['car_2']
CAR_3 = settings['google_form_alignment']['car_3']

#Preload total allocations
gt3_rem = TOTAL_GT3
gt4_rem = TOTAL_GT4
num_lead = 0 # num of lead drivers
num_team = 0 # num of team drivers

discord_id_list = []


log("-----------------------------------")
log("ACC CSV to JSON Entrylist Converter")
log("-----------------------------------")

log("\n AVAILABLE CARS:\n")

car_dict = settings['cars']

car_rem = array.array('I') #Instantiate car_rem array (empty)
team_nums = array.array('I') #Instantiate team_nums array (empty)

#Init car_rem array
for car in car_dict:
    car_rem.append(TOTAL_CAR_PER_TYPE) #Initialize a new per-type value
    if(bool(car_dict[car])):
        log(str(car) + ': ' + car_dict[car])

input_csv = ''
output_json = 'entrylist.json'
arguments = len(sys.argv) - 1
if(arguments < 1):
    log('USAGE: acc_csv_to_json.py <inputfile.csv> <admin STEAM_ID (optional)>')
    sys.exit(2)  
input_csv = sys.argv[1]

#try:
#    admin_steam_id = sys.argv[2]
#    log('\nAdmin declared as ' + admin_steam_id)
#except:
#    admin_steam_id = ""
#    log('\nINFO: No Admin ID Declared. If you want someone to have admin access, re-run with their S# as a 2nd argument.\n')

log('\nINFO: Input CSV: '+input_csv+'\n')
log('INFO: Output JSON: entrylist.json\n')


def car_num_lookup(car_dict, car_name):
    for car in car_dict:
        if(car_dict[car] == car_name):
            return car
    sys.exit("ERROR: CAR NOT FOUND. Tried a car named: " + car_name)

def check_car(driver, car, num):
    global gt3_rem
    global gt4_rem
    if(car_rem[car] == 0):
        log("INFO: for ", driver, " try ", num, " no cars remaining of ", car)
        return False
    else: 
        if(car < 50): #GT3
            if(gt3_rem == 0):
                log("INFO: for ", driver, " try ", num, " no GT3 remaining.")
                return False
            else:
                return True
        else: #GT4
            if(gt4_rem == 0):
                log("INFO: for ", driver, " try ",  num, " no GT4 remaining.")
                return False
            else: 
                return True

def error(message):
    global NUM_ERRORS
    global ERROR_BUF
    log(message)
    log("\n")
    NUM_ERRORS += 1
    ERROR_BUF = ERROR_BUF + "\n" + message


#Checks driver numbers to make sure there are no repeats. If it detects a repeat, throw an error
def check_nums(driver, team, num):
    other_team_lead = ""
    if(int(num) in team_nums):
        error("ERROR: the team " + team + " number " + num + " lead by " + driver + " conflicts with existing team who registered before them.")
        report_dict[team].update({'ERROR': "CAR NUMBER CONFLICT! MUST RE-REGISTER WITH NEW CAR NUMBER"})
        #exit()
    else:
        team_nums.append(int(num))

def select_car(driver, car1, car2, car3):
    if(check_car(driver, car1, 1)):
        return car1
    elif(check_car(driver, car2, 2)):
        return car2
    elif(check_car(driver, car3, 3)):
        return car3
    else:
        log("ERROR: Driver " + driver + " had no valid cars selected!")
        log("ERROR: CAR1 = ", car1)
        log("ERROR: CAR2 = ", car2)
        log("ERROR: CAR3 = ", car3)
        sys.exit()

def list_selected_cars():
    log("\n\n\nCARS SELECTED:")
    index = 0
    for car in car_rem:
        if(car_dict[index]):
            cars = TOTAL_CAR_PER_TYPE - car_rem[index]
            if(cars != 0):
                log(car_dict[index] + " : " + str(cars))
                log('\n')
        index += 1
def list_exhausted_cars():
    log("\n\n\nEXHAUSTED CARS: ")
    index = 0
    for car in car_rem:
        if(car_rem[index] == 0): 
            log(car_dict[index])
            log('\n')
        index += 1


def update_dict(old, new): #Updates the SETTINGS yaml
    #First flatten both settings and new dicts
    old = flatten(old)
    new = flatten(new)
    #Now merge (update)
    old.update(new)
    #Finally, unflatten and return the updated settings dict
    old = unflatten(old)
    return old

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
            team_name = row[TEAM].strip()
            drivername = str(row[FIRST] + " " + row[LAST])
            if(lead): #First pass
                if(row[LEAD_DRIVER] == "No"): #Not the lead driver, skip for this pass
                    continue #Skip iteration of this loop
                #Figure out if the car selection is legal
                car_num1 = car_num_lookup(car_dict, row[CAR_1])
                car_num2 = car_num_lookup(car_dict, row[CAR_2])
                car_num3 = car_num_lookup(car_dict, row[CAR_3])    
                car_num = select_car(drivername, car_num1, car_num2, car_num3)
                car_rem[car_num] -= 1
                gt3 = car_num < 50
                if(gt3):
                    gt3_rem -= 1
                else: 
                    gt4_rem -= 1
                team = {}
                

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
            discord_id = row[DISCORD_ID]
            discord_id_list.append(discord_id)
            if(lead): #Team info
                team['teamName'] = team_name
                team['drivers'] = [driver]
                team['overrideDriverInfo'] = 1
            
                if(driver['playerID'] in settings['admins']):
                    team['isServerAdmin'] = 1
                else:
                    team['isServerAdmin'] = 0
                
                team['forcedCarModel'] = car_num
    
                team['raceNumber'] = int(race_num)
                entries.append(team)
                num_lead += 1
                
                
                #Add this team to the report 
                #report_dict['teams'].append({'team_name' : team_name, 'lead_driver' : drivername})
                new_dict = {team_name : {'CAR_NUMBER': race_num, 'CAR': car_dict[car_num], 'LEAD_DRIVER' : {'NAME': drivername, 'DISCORD_ID': discord_id}}}
                #report_dict.update()
                #update_dict(report_dict,new_dict)
                report_dict.update(new_dict)
                check_nums(drivername, team_name, race_num)
    
            if(not lead): #We are now iterating through the dict to add the teammates
                #num_team = 0
                for key in top_dict:
                    if(key == "entries"):
                        for i in range(len(top_dict[key])): #This is a list of dicts (each driver's form entry, prev a csv row)
                            team_race_number = int(top_dict[key][i]['raceNumber']) #Grab the dict entry race num for comparison
                            dict_team_name = top_dict[key][i]['teamName']
                            for key2 in top_dict[key][i]: #Now iterate through this driver's KEYS
                                #if(key2 == "drivers"): log("KEY2: ", key2, " race_num: ", race_num, "team_race_number: ", team_race_number)
                                if(key2 == "drivers" and int(race_num) == int(team_race_number)): #Compare the lead driver's race num with this driver
                                    #log("IN KEY2")
                                    driver['driverCategory'] = top_dict[key][i][key2][0]['driverCategory'] #Adopt the lead driver's category
                                    top_dict[key][i][key2].append(driver) #Append this driver to the lead driver's team list
                                    num_team +=1
                                    if(dict_team_name == team_name):
                                        try:
                                            if(not 'SECOND_DRIVER' in report_dict[team_name].keys()):
                                                report_dict[team_name].update({'SECOND_DRIVER': {'NAME': drivername, 'DISCORD_ID': discord_id}})
                                            elif(not 'THIRD_DRIVER' in report_dict[team_name].keys()):
                                                report_dict[team_name].update({'THIRD_DRIVER': {'NAME': drivername, 'DISCORD_ID': discord_id}})
                                            elif(not 'FOURTH_DRIVER' in report_dict[team_name].keys()):
                                                report_dict[team_name].update({'FOURTH_DRIVER': {'NAME': drivername, 'DISCORD_ID': discord_id}})                                                                                   
                                        except:
                                            error(team_name + " does not exist for driver " + drivername + " of car number " + race_num)

        if(lead): #Team info
            top_dict['configVersion'] = 1
            top_dict['entries'] = entries
            top_dict['forceEntryList'] = 1
    if(lead): 
        log("# of Lead Drivers: " + str(num_lead))
    else: 
        log("# of Teammates: " + str(num_team))
        total_drv = num_team + num_lead
        log("Total number of drivers: " + str(total_drv))

#Open the JSON output file
outfile = open(output_json, "w")
top_dict = {} #Initialize the top dict
report_dict = {} #Dict purely used for reporting

#First, form teams by applying lead drivers ONLY
read_csv_write_json(input_csv, 1)

#code.interact(local=locals()) #Jump into interactive mode

#Next, populate teams with teammates
read_csv_write_json(input_csv, 0)


print(json.dumps(top_dict, indent=4), file=outfile) #Print our dictionary out to JSON
outfile.close() #Close the JSON file

log("GT3's remaining: " + str(gt3_rem))
log("GT4's remaining: " + str(gt4_rem))
#log("Number of Lead Drivers: ", num_lead)
#log("Number of Teammate Drivers: ", num_team)
final_gt3 = int(TOTAL_GT3) - int(gt3_rem)
final_gt4 = TOTAL_GT4 - gt4_rem
log("GT3 Cars: " + str(final_gt3))
log("GT4 Cars: " + str(final_gt4))

list_selected_cars()
list_exhausted_cars()
log("\n")
def generate_report(driver_dict):
    log(str(driver_dict))

generate_report(driver_dict = top_dict)

log('DONE!')

log(str(report_dict))



report_yaml = yaml.dump(report_dict, sort_keys=False)
log(report_yaml)


log("\n")
log("DISCORD LIST:")
for name in discord_id_list:
    log("\n")
    log(name)

for key, value in report_dict.items():
    log("\n=============================\n"+key+"\n=============================\n")
    value_yaml = yaml.dump(value, sort_keys=False)
    log(value_yaml)

log("\n")

if(NUM_ERRORS):
    log("ERRORS: " + str(NUM_ERRORS) + " errors saved into ERROR.log")
    errors = f_errors.readlines()
    log(ERROR_BUF)
    f_errors.write(ERROR_BUF)
    log("\n")
    log("Taken numbers include: " + str(team_nums.tolist()))

    

log("\n\n")
now = datetime.now()
dt_string = now.strftime("%Y.%m.%d %H:%M:%S")
log("This report was generated on " + dt_string)


list_selected_cars()
list_exhausted_cars()


f_log.close()
f_errors.close()