import json

# Reads the data
with open('./champions.json') as f:
    data = json.load(f)

searchUnit = input("What champion are you looking for? ")

# Puts the units into lists by cost
unitByCost = [[] for i in range(5)]
for i in data:
    unitByCost[i['cost'] - 1].append(i) 

# Helper function, returns the unit given the name
def unitByName(name):
    for i in data:
        if i['name'] == name:
            return i 
    return -1

# Returns a dictionary with
# Key: Trait name
# Value: All units of the given cost who possess that trait
def traitsByCost(cost):
    ret = {}
    for i in unitByCost[cost - 1]:
        for trait in i['traits']:
            if trait in ret:
                if i not in ret[trait]:
                    ret[trait].append(i)
            else:
                ret[trait] = [i]
    return ret
    
# Returns the list of all units that share at least one trait with the given unit
def sharesOneTrait(unit):
    ret = []
    for i in data:
        if not set(i['traits']).isdisjoint(unit['traits']):
            ret.append(i)
    return ret;

# Actually finds the best unit(s) to use your loaded die on.  
def findBestOdds(unit):
    traitCount = traitsByCost(unit['cost'])
    # The variable "best" tracks the current best champion, and the number of units it can give
    best = [[], 60] # There are only 59 champions, so this gurantees that a result is found
    
    # Goes through every champion that shares at least one trait with the given unit
    # (if there are no shared traits, it's impossible to get the desired unit)
    for champion in sharesOneTrait(unit):
        units = set([])
        for trait in champion['traits']:
            try:
                names = [unit['name'] for unit in traitCount[trait]]
                units = units.union(set(names))
            except KeyError:
                # This is necessary because traitsByCost doesn't have keys for any trait that
                # does not have a unit of the relevant cost
                continue

        if len(units) < best[1]:
            best = [[champion['name']], len(units)]
        elif len(units) == best[1]:
            best[0].append(champion['name'])
    return best[0]
        
print("Any of the following champions will give you the best odds: ")
print(findBestOdds(unitByName(searchUnit)))
