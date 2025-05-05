# Functions and Classes for Mining Simulation

# Used to generate random mining duration time for the trucks
import random

class Station:

    line_wait_times = []
    count = [] # Keeps track of how many times the site has been unloaded successfully

    ### Station Constructor ###
    def __init__(self, line_wait=0, count=0):
        # self.mine_id = mine_id
        Station.count.append(count)
        Station.line_wait_times.append(line_wait)

    
    ### Station Methods ###
    def find_highest_count(self):
        max_cnt = max(Station.count)
        max_idx = max(range(len(Station.count)), key=lambda i: Station.count[i])
        return [max_cnt, max_idx]
    
    def find_lowest_count(self):
        min_cnt = min(Station.count)
        min_idx = min(range(len(Station.count)), key=lambda i: Station.count[i])
        return [min_cnt, min_idx]


    def print_station_results(self):
        total_cnt = sum(Station.count)
        for station_id, cnt in enumerate(Station.count):
            print('Station', station_id + 1, 'unload count:', cnt, end='\t')
            print('Station ', station_id + 1, ' unload percentage: ', 
                  round(cnt/total_cnt*100, 2), '%', sep='')
        
        max_cnt, max_idx = self.find_highest_count()
        print('Highest Performing Station: Station', max_idx + 1, 'with', max_cnt, 'unloads')

        min_cnt, min_idx = self.find_lowest_count()
        print('Lowest Performing Station:  Station', min_idx + 1, 'with', min_cnt, 'unloads')


class Truck(Station):

    # Times for each mode except 'mine'
    station_travel_time = 30 # Mining Site to Unloading Station (Minutes)
    mine_travel_time = 30 # Unloading Station to Mining Site (Minutes)
    unload_time = 5 # Unloading Time (Minutes)

    # Random Start and End Values for Mining (Hours to Minutes)
    rand_start = 1 * 60
    rand_end = 5 * 60

    # Total Unload Count
    total_unload_count = 0

    ### Truck Constructor ###
    def __init__(self, truck_id, total_time, mode='mine', count=0):
       
        ### Truck Attributes ###
        self.mode_count = {'mine' : 0, 
                          'travel_to_station' : 0, 
                          'travel_to_mine' : 0, 
                          'unload' : 0, 
                          'wait_in_line' : 0}

        self.mode = mode # mine, travel_to_station, travel_to_mine, unload, and wait_in_line
        self.mode_count[self.mode] += 1
        self.mode_time_array = [self.mode for i in range(total_time)] # For Plot
        self.truck_id = truck_id


        self.step = 0
        self.wait_time = random.randint(Truck.rand_start, Truck.rand_end) # minutes
        self.wait_time_array = [self.wait_time for i in range(total_time)] # For Plot

        self.current_station = -1 # Station Line where truck is waiting to unload or unloading (-1 means "not at any site")
        self.count = count # Count of Unloads by Truck
        self.count_time_array = [self.count for i in range(total_time)] # For Plot
    
    ### Truck Methods ###

    # Determines shortest site line to unload
    def find_shortest(self):
        shortest_wait = int(1e18) # Large Value Initialiazed to Find Shortest Line Wait
        for station_id, wait in enumerate(Station.line_wait_times):
            if wait == 0:
                return [station_id, wait]
            
            if wait < shortest_wait:
                shortest_wait = wait
                station_short = station_id

        return [station_short, shortest_wait]

    def activity_step(self):
        self.wait_time -= 1
        self.step += 1
        for station_id, wait in enumerate(Station.line_wait_times):
            if wait > 0:
                Station.line_wait_times[station_id] -= 1 # Decrease Station Wait Time for Station

        if self.wait_time <= 0:
            self.transition() # determine transition

        # Update Mode Counter
        self.mode_count[self.mode] += 1
        
        # Update Time Array for Plots
        self.count_time_array[self.step] = self.count
        self.wait_time_array[self.step] = self.wait_time
        self.mode_time_array[self.step] = self.mode
    
    def transition(self):
        if self.mode == 'mine':
            self.mode = 'travel_to_station'
            self.wait_time = Truck.station_travel_time

        elif self.mode == 'travel_to_station':
            station_short, shortest_wait = self.find_shortest()
            if shortest_wait == 0:
                self.mode = 'unload'
                self.wait_time = Truck.unload_time
            else:
                self.mode = 'wait_in_line'
                self.wait_time = Station.line_wait_times[station_short]

            Station.line_wait_times[station_short] += Truck.unload_time
            self.current_station = station_short
            

        elif self.mode == 'wait_in_line':
            self.mode = 'unload'
            self.wait_time = Truck.unload_time
        
        elif self.mode == 'unload':
            self.count += 1
            Truck.total_unload_count += 1
            Station.count[self.current_station] += 1
            self.current_station = -1
            self.mode = 'travel_to_mine'
            self.wait_time = Truck.mine_travel_time

        elif self.mode == 'travel_to_mine':
            self.mode = 'mine'
            self.wait_time = random.randint(Truck.rand_start, Truck.rand_end)

    def print_truck_state(self):
        print('Truck', self.truck_id,'Current Mode --->  ', self.mode, end='\t')
        print('Truck', self.truck_id,'Current Wait Time --->  ', self.wait_time)

    
    def print_truck_results(self):
        print('Truck', self.truck_id, 'results ---> Unload Count:', self.count, end='\t')
        print('Unload Percentage: ', round(self.count/Truck.total_unload_count*100, 2), '%', sep='')