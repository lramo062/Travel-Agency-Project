import socket
import sys
from _thread import *
from multiprocessing import Process, Lock

def initialize_flights():
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

# returns a string of all the flight info from the flights dict
def list_all(flights):
    info = ''
    for f in flights:
        info += f + ' ' + flights[f] + '\n'
    return info

# returns a string of the flight info from matching keys in flights dict
def list(keys, flights):
    info = ''
    for k in keys:
        info += k + ' ' + flights[k] + '\n'
    return info

# returns a list of keys with matching to destination
def search_destination(dest, flights):
    dest = '-' + dest
    flight_keys = flights.keys()
    matched_keys = []
    for k in flight_keys:
        if dest in k:
            matched_keys.append(k)
    return matched_keys

# returns a list of keys with matching departures
def search_departure(dep, flights):
    dep = dep + '-'
    flight_keys = flights.keys()
    matched_keys = []
    for k in flight_keys:
        if dep in k:
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

# buy x amount of tickets for a route
def buy_ticket(route, number_of_tickets, flights):
    seats = int(flights[route].split(None,1)[0])
    number_of_tickets = int(number_of_tickets)
    price = flights[route].split(None,1)[1]
    updated_seats = seats - number_of_tickets
    if (updated_seats >= 0):
        flights[route] = str(seats - number_of_tickets) + ' ' + price
        return "Thank you for purchasing " + str(number_of_tickets) + " ticket(s)\n"
    else:
        return "Sorry we do not have that many tickets available\n"

# return x amount of tickets for a route
def return_ticket(route, number_of_tickets, flights):
    seats = int(flights[route].split(None,1)[0])
    number_of_tickets = int(number_of_tickets)
    price = flights[route].split(None,1)[1]
    flights[route] = str(seats + number_of_tickets) + ' ' + price
    return "Thank you for returning " + str(number_of_tickets) + " ticket(s)\n"

# buy x amount of tickets for a round trip route
def buy_round_trip_ticket(route, number_of_tickets, flights):
    r_route = route.split('-',1)[1] + '-' + route.split('-',1)[0]

    seats = int(flights[route].split(None,1)[0])
    r_seats = int(flights[r_route].split(None,1)[0])
    number_of_tickets = int(number_of_tickets)

    price = flights[route].split(None,1)[1]
    r_price = flights[r_route].split(None,1)[1]

    updated_seats = seats - number_of_tickets
    updated_r_seats = r_seats - number_of_tickets
    if (updated_seats >= 0 and updated_r_seats >=0):
        flights[route] = str(seats - number_of_tickets) + ' ' + price
        flights[r_route] = str(r_seats - number_of_tickets) + ' ' + r_price
        return "Thank you for purchasing " + str(number_of_tickets) + " ticket(s)\n"
    else:
        return "Sorry we do not have that many tickets available for one or both of your routes\n"

# return x amount of tickets for a round trip route
def return_round_trip_ticket(route, number_of_tickets, flights):
    r_route = route.split('-',1)[1] + '-' + route.split('-',1)[0]

    seats = int(flights[route].split(None,1)[0])
    r_seats = int(flights[r_route].split(None,1)[0])
    number_of_tickets = int(number_of_tickets)

    price = flights[route].split(None,1)[1]
    r_price = flights[r_route].split(None,1)[1]
    flights[route] = str(seats + number_of_tickets) + ' ' + price
    flights[r_route] = str(r_seats + number_of_tickets) + ' ' + r_price
    return "Thank you for returning " + str(number_of_tickets) + " ticket(s)\n"
    
def command_handler(command, flights):
    error_message = "Unexpected Command, please enter a valid command\n"

    # LIST COMMAND
    if command == 'LIST':
        return list_all(flights)

    # SEARCHD COMMAND
    elif 'SEARCHD ' in command:
        try:
            if command.split(None,1)[1]:
                keys = search_destination(command.split(None,1)[1], flights)
                if not keys:
                    return "no flights matched your criteria\n"
                else:
                    return list(keys, flights)
        except:
            return error_message

    # SEARCHDEPARTURE COMMAND
    elif 'SEARCHDEPARTURE ' in command:
        try:
            if command.split(None,1)[1]:
                keys = search_departure(command.split(None,1)[1], flights)
                if not keys:
                    return "no flights matched your criteria\n"
                else:
                    return list(keys, flights)
        except:
            return error_message

    # SEARCHALL COMMAND
    elif 'SEARCHALL ' in command:
        try:
            if command.split(None,1)[1]:
                keys = search_all_destination(command.split(None,1)[1], flights)
                if not keys:
                    return "no flights matched your criteria\n"
                else:
                    return list(keys, flights)
        except:
            return error_message

    # BUY_TICKET COMMAND
    elif 'BUY_TICKET ' in command:
        split_command = command.split(None,2)
        try:
            if split_command[2]:
                return buy_ticket(split_command[1], split_command[2], flights)
        except:
            return error_message

    # BUYRT_TICKET COMMAND
    elif 'BUYRT_TICKET ' in command:
        split_command = command.split(None,2)
        try:
            if split_command[2]:
                return buy_round_trip_ticket(split_command[1], split_command[2], flights)
        except:
            return error_message

    # RETURN_TICKET COMMAND
    elif 'RETURN_TICKET ' in command:
        split_command = command.split(None,2)
        try:
            if split_command[2]:
                return return_ticket(split_command[1], split_command[2], flights)
        except:
            return error_message

    # RETURNRT_TICKET COMMAND
    elif 'RETURNRT_TICKET ' in command:
        split_command = command.split(None,2)
        try:
            if split_command[2]:
                return return_round_trip_ticket(split_command[1], split_command[2], flights)
        except:
            return error_message
    else:
        return error_message

# Function for handling connections. This will be used to create threads
def clientthread(conn, flights):
    # infinite loop so threads don't exit
    while True:
        # Receiving from client
        data = conn.recv(1024).decode()
        if not data: 
            break
        else:
            # create mutex lock
            mutex.acquire()
            try:
                conn.send(command_handler(data, flights).encode())
            finally: # release mutex
                mutex.release()
    # came out of loop
    conn.close()

HOST = 'localhost'
PORT = 10000

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind socket to local host and port, print if fails
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
      
# Start listening on socket
s.listen(10)

  # Initialize Flight Data
flights = initialize_flights()
mutex = Lock()

# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientthread,(conn, flights,))
        
s.close()
