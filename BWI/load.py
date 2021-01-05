#!/usr/bin/env python3
import itertools
import json
import copy
import math
import datetime
from colorama import Fore, Back, Style

def calcw(transporter):
    return sum([i["amount"]*i["weight"] for i in transporter["items"]]) + transporter["driver"]["weight"]

def calcws(transporters):
    for transporter in transporters:
        transporter["load"] = calcw(transporter)

def calcv(transporter):
    return sum([i["amount"]*i["value"] for i in transporter["items"]])

def calca(transporter):
    return sum([i["amount"] for i in transporter["items"]])

def calc_items(transporters, items):
    return sum([calca(t) for t in transporters]) \
     + sum([i["amount"] for i in items])

def calcvs(transporters):
    for transporter in transporters:
        transporter["acc_value"] = calcv(transporter)

def calc_combinations_value(transporters):
    return sum([t["acc_value"] for t in transporters])

def remove_zero_items_once(transporter):
    [item for item in transporter["items"] if item["amount"] > 0]

def remove_zero_items(transporters):
    for transporter in transporters:
        remove_zero_items_once(transporter)

def check_self(transporters, items, itemcount):
    assert itemcount == calc_items(transporters, items)
    for transporter in transporters:
        assert transporter["load"] == calcw(transporter)
        assert transporter["capacity"] >= transporter["load"]
        assert transporter["driver"] != None
        assert transporter["acc_value"] == calcv(transporter)
        for item in transporter["items"]:
            assert item["amount"] >= 0
    for item in items:
            assert item["amount"] >= 0

def check_self_short(transporters, items):
    for transporter in transporters:
        assert transporter["load"] == calcw(transporter), f"{transporter['load']} != {calcw(transporter)}"
        assert transporter["capacity"] >= transporter["load"]
        assert transporter["driver"] != None
        assert transporter["acc_value"] == calcv(transporter)
    

def unload(transporter, items, item):
    for load_item in transporter["items"]:
        if load_item["name"] == item["name"]:
            if item["amount"] <= load_item["amount"]:
                load_item["amount"] -= item["amount"]
            else:
                return False
    transporter["acc_value"] -= item["amount"] * item["value"]
    transporter["load"] -= item["amount"] * item["weight"]
    for deposit_item in items: # add back to deposit items
        if deposit_item["name"] == item["name"]:
            deposit_item["amount"] += item["amount"]
    remove_zero_items_once(transporter)
    return True

def load(transporter, items, item):
    if transporter["load"] + item["amount"] * item["weight"] > transporter["capacity"]:
        return False
    for deposit_item in items:
        if deposit_item["name"] == item["name"]:
            if item["amount"] <= deposit_item["amount"]:
                deposit_item["amount"] -= item["amount"]
            else:
                return False
    
    for transp_item in transporter["items"]:
        if transp_item["name"] == item["name"]:
            transp_item["amount"] += item["amount"]
            break
    else:
        transporter["items"] += [item]
    transporter["acc_value"] += item["amount"] * item["value"]
    transporter["load"] += item["amount"] * item["weight"]
    return True



def try_replacing(transporters, items):
    check_self_short(transporters, items)
    combinations_value = 0
    for transporter in transporters:
        for item in items:
            if item["amount"] > 0:
                avaliable_space = transporter["capacity"] - transporter["load"]
                if avaliable_space >= 0:
                    desired_free = item["weight"] - avaliable_space
                    if desired_free > 0:
                        for loaditem in transporter["items"]:
                            if item["name"] != loaditem["name"]:
                                free_amount = desired_free/loaditem["weight"]
                                free_amount = math.ceil(free_amount)
                                if loaditem["amount"] >= free_amount:
                                    if free_amount * loaditem["value"] <= item["value"]:
                                        removeitem = copy.deepcopy(loaditem)
                                        removeitem["amount"] = free_amount
                                        if unload(transporter, items, removeitem):
                                            additem = copy.deepcopy(item)
                                            additem["amount"] = 1
                                            if not load(transporter, items, additem):
                                                assert load(transporter, items, removeitem) # reload, but should never happen
                                            else:
                                                combinations_value = calc_combinations_value(transporters)

    return combinations_value, transporters, items


def find_max(transporters, items):
    check_self_short(transporters, items)
    for transporter in transporters:
        for item in items: # start loading the best value per weight items
            avaliable_space = transporter["capacity"] - transporter["load"]
            if avaliable_space > 0:
                desired_amount = min(int(avaliable_space/item["weight"]), item["amount"]) # take everything that fits or as much as avaliable
                if desired_amount > 0: # so we don't spam the load list of the transporter with amount=0 items
                    loaditem = copy.deepcopy(item)
                    loaditem["amount"] = desired_amount
                    assert load(transporter, items, loaditem)
                    
    
    combinations_value = calc_combinations_value(transporters)
    return  combinations_value, transporters, items

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

    while len(drivers) < len(transporters): # keep the transporters with the most capacity with drivers avaliable
        del transporters[-1]

    while len(drivers) > len(transporters): # keep the lightes drivers
        del drivers[-1]
        

    max_value = 0
    max_transporters = None
    max_items = None
    itemcount = calc_items(transporters, items)

    try:# we can't bruteforce every combinations for the items, becaue there are too many possibilities
        for transporters_possible in itertools.permutations(transporters): # but at least we can bruteforce the order of transporters to use
            for drivers_possible in itertools.permutations(drivers):  # and the mapping between drivers and transporters
                transporters_copy = copy.deepcopy(transporters_possible) # every element in list is an object so just copy is not enough
                for i in range(len(transporters)):
                    transporters_copy[i]["load"] += drivers_possible[i]["weight"]
                    transporters_copy[i]["driver"] = drivers_possible[i]

                combinations_value, combinations_transporters, combination_items = find_max(transporters_copy, copy.deepcopy(items))
                combinations_value, combinations_transporters, combination_items = try_replacing(combinations_transporters, combination_items) # calculate the maximum

                if combinations_value > max_value:
                    max_value = copy.deepcopy(combinations_value)
                    max_transporters = copy.deepcopy(combinations_transporters)
                    max_items = copy.deepcopy(combination_items)
                    print(f"Max Value achieved: {max_value}", end="\r") # show progress
    except KeyError as ke:
        print(Fore.RED + f"KeyError encounterd has the json data the right structure? {str(ke)}" + Style.RESET_ALL)

    print(f"Max Value achieved: {max_value}")
    if max_value > 0:
        check_self(max_transporters, max_items, itemcount)
        print(f"Weight transported per transporter in % of capacity: {[math.floor(transp['load']/transp['capacity']*100000)/1000 for transp in max_transporters]}")
        print(f"Total weight use in %: {math.floor(sum([transp['load'] for transp in max_transporters])/sum([transp['capacity'] for transp in max_transporters])*100000)/1000}")
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