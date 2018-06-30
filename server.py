def initializeFlights():
    # read flights.txt file
    path = './flights.txt'
    flights = open(path, 'r').read().splitlines()

    # generate return flights
    rflights = []
    for f in flights:
        destinations = f.split(None, 1)[0].split('-')
        info = f.split(None, 1)[1]
        rflights.append(destinations[1] + '-' + destinations[0] + ' ' + info)
    flights = flights + rflights

    # create dictionary
    flight_dict = {}
    for f in flights:
        destinations = f.split(None, 1)[0]
        info = f.split(None, 1)[1]
        flight_dict[destinations] = info
    return flight_dict

# returns all the flight info from the flights dict
def list(flights):
    for f in flights:
        print(f, flights[f])

# returns all the flight info from matching keys in flights dict
def list(keys, flights):
    for k in keys:
        print(k, flights[k])

# returns a list of keys with matching to destination
def search_destination(dest, flights):
    dest = '-' + dest
    flight_keys = flights.keys()
    matched_keys = []
    for k in flight_keys:
        if dest in k:
            matched_keys.append(k)
    return matched_keys

# returns a list of keys with matching to/from destinations
def search_all_destination(dest, flights):
    flight_keys = flights.keys()
    matched_keys = []
    for k in flight_keys:
        if dest in k:
            matched_keys.append(k)
    return matched_keys
