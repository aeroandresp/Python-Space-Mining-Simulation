# Unit Tests for Mining Sim
import mining_sim_functions as sim

tests_passed = 0
tests_failed = 0
failed_cases = []

total_time = 72*60

m = 5

truck = sim.Truck(1, total_time)
stations = [sim.Station() for station in range(m)]

for i in range(m):
    stations[0].count[i] = i*2

max_cnt, max_idx = stations[0].find_highest_count()
min_cnt, min_idx = stations[0].find_lowest_count()

### Station Method Test 1 ###
if max_cnt == 8 and max_idx == 4:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Highest Count Function: max_cnt is ' + max_cnt, ' and max_idx is ' + max_idx
    failed_cases.append(msg)

### Station Method Test 2 ###
if min_cnt == 0 and min_idx == 0:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Lowest Count Function: min_cnt is ' + min_cnt, ' and min_idx is ' + min_idx
    failed_cases.append(msg)

### Truck Method Test 1 ###
stations[0].line_wait_times[0] = 4
stations[0].line_wait_times[1] = 7
stations[0].line_wait_times[2] = 9
stations[0].line_wait_times[3] = 3
stations[0].line_wait_times[4] = 2 # Shortest Wait
# print(stations[0].line_wait_times)
station_short, shortest_wait = truck.find_shortest()

if station_short == 4 and shortest_wait == 2:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Find Shortest Function: station_short is ' + str(station_short) + ' and station_wait is ' + str(shortest_wait)
    failed_cases.append(msg)

### Truck Method Test 2 ###
stations[0].line_wait_times[0] = 2
stations[0].line_wait_times[1] = 1
stations[0].line_wait_times[2] = 0
stations[0].line_wait_times[3] = 5
stations[0].line_wait_times[4] = 6 # Shortest Wait
# print(stations[0].line_wait_times)
station_short, shortest_wait = truck.find_shortest()

if station_short == 2 and shortest_wait == 0:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Find Shortest Function: station_short is ' + str(station_short) + ' and station_wait is ' + str(shortest_wait)
    failed_cases.append(msg)

### Truck Method Test 3 ###
step = truck.step
wait_time = truck.wait_time

# Go to next time step
truck.activity_step()

if truck.step == step + 1 and truck.wait_time == wait_time - 1:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Activity Step Function: step and/or time did not change as expected'
    failed_cases.append(msg)

### Truck Method Test 4 ###
mode = truck.mode

truck.transition()

if mode != truck.mode:
    tests_passed += 1
else:
    tests_failed += 1
    msg = 'Failed Transition Function: mode did not change as expected'
    print(msg)

### Future Unit Test Additions if Given More Time and Resources ###
# 1. Test Truck method, transition, to check all mode transitions
# 2. Test Truck method, activity_step, to check that Truck.wait_time is always a positive integer value
# 3. Test Truck method, activity_step, to check all truck attributes change to their correct value as expected
# 4. Use a framework like pytest to properly unit test this Mining Sim for readability and scalability

print('Tests Passed:' ,tests_passed)
print('Tests Failed:' ,tests_failed)
print(failed_cases) if failed_cases else print('All Cases Passed')