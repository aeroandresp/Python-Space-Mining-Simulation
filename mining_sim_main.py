# Mining Simulation
import mining_sim_functions
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys

def main():

    n = 100 # Number of Mining Trucks
    m = 1 # Number of Unloading Stations

    # Results Text File
    results_filename = 'truck_results.txt'
    sys.stdout = open(results_filename, 'w')
    
    # Plot Variables
    plots = True # Create Plots (True) or not (False)
    plot_filename = 'mining_sim_plots.pdf'
    width = 16
    height = 14
    
    # Time Variables
    total_time = int(72*60) # Total Simlultion Time from Hours to Minutes
    total_time_array = [t/60 for t in range(total_time)] # Each Element in Hour

    # Object Initialization
    trucks = [mining_sim_functions.Truck(truck + 1, total_time) for truck in range(n)]
    stations = [mining_sim_functions.Station() for station in range(m)]

    # Run Simulation (Start at t = 1 since t = 0 is already initialized)
    for t in range(1, total_time):
        for truck in trucks:
            truck.activity_step()

    print('Number of Trucks:', n)
    print('Number of Stations:', m)
    print('\n\n')
    
    print("Print Station Results")
    trucks[0].print_station_results()
    print('\n\n')

    print("Print Truck Results")

    # Find Highest and Lowest Performing Truck
    best_cnt = 0
    worst_cnt = int(1e18)

    for truck in trucks:
        truck.print_truck_results()

        if truck.count > best_cnt:
            best_cnt = truck.count
            best_truck = truck.truck_id

        if truck.count < worst_cnt:
            worst_cnt = truck.count
            worst_truck = truck.truck_id

    print('Best Performing Truck: Truck', best_truck, 'with', best_cnt, 'unloads')
    print('Worst Performing Truck: Truck', worst_truck, 'with', worst_cnt, 'unloads')

    # Start Printing onto Terminal Again
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    print('File --->', results_filename, 'has been created!')

    if plots:
        i = 0 # Track Progress of PDF Creation
        with PdfPages(plot_filename) as pdf: # Save Plots to PDF
            for truck in trucks:

                i += 1
                if i != n:
                    print(f'PDF Creation Progress: {i}/{n}', end='\r', flush=True)
                else:
                    print(f'PDF Creation Progress: {i}/{n}')

                # Subplots per Page Within PDF File
                fig, axs = plt.subplots(3, 1, figsize=(width, height))

                # Plot 1
                modes = truck.mode_count.keys()
                time_count = truck.mode_count.values()
                wedges, _, _ = axs[0].pie(time_count, autopct='%1.1f%%', labels=modes, startangle=220, 
                                          labeldistance=1.7, pctdistance=1.3)
                axs[0].legend(wedges, modes, title="Modes", loc="center left", bbox_to_anchor=(1, 0.5))
                axs[0].set_title(f'Percentage of Time Spent for Truck {truck.truck_id}')
                axs[0].axis('equal')
                
                # Plot 2
                axs[1].plot(total_time_array, truck.mode_time_array)
                axs[1].set_xlabel('Time (Hours)')
                axs[1].set_ylabel('Truck Mode')
                axs[1].set_title(f'Truck {truck.truck_id} Mode vs Time')

                # Plot 3
                axs[2].plot(total_time_array, truck.count_time_array)
                axs[2].set_xlabel('Time (Hours)')
                axs[2].set_ylabel('Truck Unload Count')
                axs[2].set_title(f'Truck {truck.truck_id} Unload Count vs Time')


                plt.tight_layout()

                pdf.savefig()
                plt.close()

        print('File --->', plot_filename, 'has been created!')

# Start Script Here
if __name__ == '__main__':
    main()
