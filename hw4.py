import county_demographics
import sys

from build_data import convert_county
from data import CountyDemographics

def display(county: CountyDemographics):
    print(f"{county.county}, {county.state}")
    print("Population:")
    for i in county.population:
        print("\t{}: {}". format(i, county.population[i]))
    print("Age:")
    for i in county.age:
        print("\t{}: {}".format(i, county.age[i]))
    print("County:")
    print(f"    County: {county.county}")

    print("Education:")
    for i in county.education:
        print("\t:{}: {}".format(i, county.education[i]))

    print("Ethnicities:")
    for i in county.ethnicities:
        print("\t:{}: {}".format(i, county.ethnicities[i]))

    print("Income:")
    for i in county.income:
        print("\t:{}: {}".format(i, county.income[i]))

    print ("State:")
    print(f"    State: {county.state}")

def filter_state(scope, state):
    scope1 = []
    for i in scope:
        if i.state == state:
            scope1.append(i)
    return scope1

def filter_gt(scope, field, num):
    scope1 = []
    filtered_array = field.split(".")
    for i in scope:
        if filtered_array[0] == "Education":
            if i.education[filtered_array[1]] > num:
                scope1.append(i)
        if filtered_array[0] == "Ethnicities":
            if i.ethnicities[filtered_array[1]] > num:
                scope1.append(i)
        if filtered_array[0] == "Income":
            if i.income[filtered_array[1]] > num:
                scope1.append(i)
    return scope1

def filter_lt(scope, field, num):
    filtered_array = field.split(".")
    scope1 = []

    for i in scope:
        if filtered_array[0] == "Education":
            if i.education[filtered_array[1]] < num:
                scope1.append(i)
        if filtered_array[0] == "Ethnicities":
            if i.ethnicities[filtered_array[1]] < num:
                scope1.append(i)
        if filtered_array[0] == "Income":
            if i.income[filtered_array[1]] < num:
                scope1.append(i)
    return scope1

def population_total(scope):
    total = 0
    try:
        for i in scope:
            total += i.population['2014 Population']
        print("2014 population: {}".format(total))
    except KeyError as e:
        print(e)
    return total

def population(scope, field):
    filtered_array = field.split(".")
    total = 0
    for i in scope:
        if filtered_array[0] == "Education":
            total += i.population['2014 Population'] * i.education[filtered_array[1]]
        if filtered_array[0] == "Ethnicities":
            total += i.population['2014 Population'] * i.ethnicities[filtered_array[1]]
        if filtered_array[0] == "Income":
            total += i.population['2014 Population'] * i.income[filtered_array[1]]
    return total

def percent(scope, field):
    filtered_array = field.split(".")
    total = 0
    sub_tot = 0
    for county in scope:
        try:
            if filtered_array[0] == "Education":
                total += county.population['2014 Population']
                sub_tot += county.population['2014 Population'] * (county.education[filtered_array[1]] / 100)
            elif filtered_array[0] == "Ethnicities":
                total += county.population['2014 Population']
                sub_tot += county.population['2014 Population'] * (county.ethnicities[filtered_array[1]] / 100)
            elif filtered_array[0] == "Income":
                total += county.population['2014 Population']
                sub_tot += county.population['2014 Population'] * (county.income[filtered_array[1]] / 100)
        except KeyError as e:
            print(f"KeyError for field '{field}' in county {county.county}. Skipping.")
            continue

    if total == 0:
        return 0.0
    return (sub_tot / total) * 100

def operation():
    entry = 0
    line = 0
    try:
        f = open(str(sys.argv[1]))
        data = open("county_demographics.data")
        counties = [convert_county(county) for county in county_demographics.get_report()]
        scope = counties
        entry = len(counties)
        print("{} records loaded". format(entry))
        for i in f:
            operation1 = i.split(":")
            for x in range(len(operation1)):
                if "/n" in operation1[x]:
                    operation1[x] = operation1[x][:-1]

            if operation1[0] == "display":
                for x in scope:
                    display(x)
            elif operation1[0] == "filter-state":
                scope = filter_state(scope, operation1[1])
                print("Filter: state == {} ({} entry)".format(operation1[1], len(scope)))
            elif operation1[0] == "filter-gt":
                try:
                    scope = filter_gt(scope, operation1[1], float(operation1[2]))
                    print("Filter: {} > {} ({} entry)".format(operation1[1], operation1[2], len(scope)))
                except:
                    print("Arguments invalid.")
            elif operation1[0] == "filter-lt":
                try:
                    scope = filter_lt(scope, operation1[1], float(operation1[2]))
                    print("Filter: {} < {} ({}entry)".format(operation1[1], operation1[2], len(scope)))
                except:
                    print("Arguments invalid.")
            elif operation1[0] == "total population":
                population_total(scope)

            elif operation1[0] == "population":
                print("2014 {} population: {}".format(operation1[1], population(scope,operation1[1])))
            elif operation1[0] == "percent":
                print("2014 {} percentage: {}".format(operation1[1], percent(scope, operation1[1])))
            else:
                print("Can not read operation")
            line += 1
        f.close()
        data.close()
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    operation()
