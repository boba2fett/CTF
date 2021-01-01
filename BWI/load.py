#!/usr/bin/env python3
import itertools
import json
import copy
import math
import datetime
from colorama import Fore, Back, Style

def find_max(transporters, items):
        for transporter in transporters:
            for item in items: # start loading the best value per weight items
                avaliable_space = transporter["capacity"] - transporter["load"]
                desired_amount = min(int(avaliable_space/item["weight"]), item["amount"]) # take everything that fits or as much as avaliable
                if desired_amount > 0: # so we don't spam the load list of the transporter with amount=0 items
                    loadeditem = item.copy()
                    item["amount"] -= desired_amount
                    loadeditem["amount"] = desired_amount
                    transporter["load"] += desired_amount * item["weight"]
                    transporter["items"] += [loadeditem]
                    transporter["acc_value"] += desired_amount * item["value"]
        
        combinations_value = sum([transporter["acc_value"] for transporter in transporters])
        return combinations_value, transporters

def main(datafile: ("datafile to read data from"), output: ("output loadlist to specified file", 'option', 'o')):
    """Calculates the best load list for a specified data file in json format"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
    print(Fore.CYAN + f"started: {timestamp}" + Style.RESET_ALL)

    # load data from data.json
    try:
        f=open(datafile)

        data=json.loads(f.read())
        try:
            transporters=data["transporters"]
            drivers=data["drivers"]
            items=data["items"]
        except Exception as ex:
            raise Exception("json data doesn't have the required elements, which are: transporters, drivers, items") # more speaking error message for wrong json data

        f.close()
    except Exception as ex:
        print(Fore.RED + f"Reading in data failed, because: {str(ex)}" + Style.RESET_ALL)
        exit(1)

    items.sort(key=lambda item: item['value']/item['weight'], reverse=True) # sort by value per weight
    transporters.sort(key=lambda t: t["capacity"], reverse=True)
    drivers.sort(key=lambda d: d["weight"])

    while len(drivers)<len(transporters): # keep the transporters with the most capacity with drivers avaliable
        del transporters[-1]

    while len(drivers)>len(transporters): # keep the lightes drivers
        del drivers[-1]
        

    max_value = 0
    max_transporters = None

    try:# we can't bruteforce every combinations for the items, becaue there are too many possibilities
        for transporters_possible in itertools.permutations(transporters): # but at least we can bruteforce the order of transporters to use
            for drivers_possible in itertools.permutations(drivers):  # and the mapping between drivers and transporters
                transporters_copy = copy.deepcopy(transporters_possible) # every element in list is an object so just copy is not enough
                for i in range(len(transporters)):
                    transporters_copy[i]["load"] += drivers_possible[i]["weight"]
                    transporters_copy[i]["driver"] = drivers_possible[i]

                combinations_value, combinations_transporters = find_max(transporters_copy, copy.deepcopy(items)) # calculate the maximum

                if combinations_value > max_value:
                    max_value = combinations_value
                    max_transporters = combinations_transporters
                    print(f"Max Value achieved: {max_value}", end="\r") # show progress
    except KeyError as ke:
        print(Fore.RED + f"KeyError encounterd has the json data the right structure? {str(ke)}" + Style.RESET_ALL)

    print(f"Max Value achieved: {max_value}")
    if max_value > 0:
        print(f"Weight transported per transporter in % of capacity: {[math.floor(transp['load']/transp['capacity']*10000)/100 for transp in max_transporters]}")
        print(f"Total weight use in %: {math.floor(sum([transp['load'] for transp in max_transporters])/sum([transp['capacity'] for transp in max_transporters])*10000)/100}")
        print("Load List:")
        data_json=json.dumps(max_transporters, indent=4)
        print(data_json)
        if output:
            try:
                f=open(output,"w")
                f.write(data_json)
                f.close()
                print(Fore.CYAN + "Load List saved in loadlist.json" + Style.RESET_ALL)
            except Exception as ex:
                print(Fore.YELLOW + f"Load List could not be saved in loadlist.json, becase: {str(ex)}" + Style.RESET_ALL)

    else:
        print(Fore.YELLOW + "No solution found" + Style.RESET_ALL)
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
    print(Fore.CYAN + f"exited: {timestamp}" + Style.RESET_ALL)

if __name__ == '__main__':
    import plac
    plac.call(main)