import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from itertools import accumulate
import tkinter as tk
from tkinter import *
import sys

# Connects to the database to retrieve latest data collected from the webscraper
conn = sqlite3.connect('COVID_Webscraper/case_data.db')
curr = conn.cursor()

# Selects all countries from database
curr.execute("SELECT country_name FROM cases_tb")
countries = curr.fetchall()

# Only takes the country element from each array
for element_number in range(len(countries)):
    countries[element_number] = countries[element_number][0]

# Initialize user interface
window = Tk()
window.title("Settings")
window.geometry("270x100")


# Terminates the program if the user indicates they would like to exit
def exit_program():
    sys.exit(0)


# Saves the country selected by the user
def country_click(*args):
    global country_dropdown
    country_dropdown = clicked_country.get()


# Initializes the second window for the UI
def next_page():
    global duration
    global state

    # Ensures user selects a country
    if clicked_country.get() == "Choose a country":
        messagebox.showerror("Error", "Select a country")
    else:
        
        # Checks whether the interval is an integer
        try:
            int(intervals.get())/1
        
        # Alerts user if entry is not an integer
        except:
            messagebox.showerror("Error", "Ensure that you have entered an integer")

        else:
            duration = []
            state = []

            # Removes all widgets from the window
            for widget in window.winfo_children():
                widget.destroy()

            # Adds new widgets to the window
            for condition_number in range(int(intervals.get())):

                # Stores user entries
                duration.append(StringVar())
                state.append(StringVar())

                # Initial value of restrictions
                state[condition_number].set("Restrictions")

                # Labels each entry with the prompt 'Interval'
                if condition_number == 0:
                    Label(window, text=("Interval " + str(condition_number+1) + " (days)")).grid(columnspan=2)
                else:
                    Label(window, text=("Interval " + str(condition_number+1))).grid(columnspan=2)

                # Entry and dropdown module that stores selections from user
                Entry(window, textvariable=duration[-1]).grid(row=condition_number, column=2, columnspan=3, sticky="ew")
                OptionMenu(window, state[-1], "Lockdown", "Vacation", "School closure", "No restrictions").grid(row=condition_number, column=5, columnspan=2, padx=3)

            # Buttons to end the program or move on to producing a graph
            finish_button = Button(window, text="Finish", command=duration_state).grid(row=int(intervals.get()), column=1, columnspan=2, sticky="ew", pady=10)
            exit_button = Button(window, text="Exit", command=exit_program).grid(row=int(intervals.get()), column=4, columnspan=2, sticky="ew", pady=10)
            
            # Increases the window size to match user inputs
            window.geometry("350x" + str(31*int(intervals.get()) + 40))


# Closes the second window
def duration_state():

    # Loop runs through the values provided for each input of the second window
    for entry in range(int(intervals.get())):

        # Checks whether all interval entries are integers
        try:
            int(duration[entry].get())/1

        # Alerts the user if an integer is not given
        except:
            messagebox.showerror("Error", "Ensure that you have entered integers for all entries")
            break

        # Alerts the user if no restriction is placed for an interval entry
        if state[entry].get() == "Restrictions":
            messagebox.showerror("Error", "Ensure that a restriction is applied to each interval")
            break

        # If all entries are valid, the program continues and the window is cleared
        if entry == int(intervals.get()) - 1:
            window.destroy()


# Solves the system of differential equations for the SEIR model
def differential(initial, time, *args):

    # Holds initial conditions for the population
    susceptible, exposed, infected, recovered = initial

    # System of differential equations
    # Represents changes in the susceptible, exposed, infected, and recovered population
    dSdt = -(beta * susceptible * infected) / POPULATION_SIZE
    dEdt = beta * susceptible * infected / POPULATION_SIZE - SIGMA * exposed
    dIdt = SIGMA * exposed - GAMMA * infected
    dRdt = GAMMA * infected

    return dSdt, dEdt, dIdt, dRdt


# Variables to store values from user entries for first window
clicked_country = StringVar()
intervals = StringVar()

# Provides user with a prompt
clicked_country.set("Choose a country")

country_label = Label(window, text="Country:").grid()

# Provides a dropdown menu to select a country from a list provided by the database
drop = OptionMenu(window, clicked_country, *countries).grid(row=0, column=1, columnspan=4, sticky=W)

interval_number_label = Label(window, text="Number of Intervals:").grid(row=1, column=0)

# Provides entry module to store the number of intervals used for the second window
interval_number_entry = Entry(window, textvariable=intervals).grid(row=1, column=1, columnspan=5)

# Allows the user to either exit the program or move to the next window
next_button = Button(window, text="Next", command=next_page).grid(row=3, column=1, sticky="ew", pady=10)
exit_button = Button(window, text="Exit", command=exit_program).grid(row=3, column=3, sticky="ew", pady=10)

# Tracks whether the user selects a country
clicked_country.trace('w', country_click)

window.mainloop()

# Selects the data from the row from the selected country
curr.execute("SELECT * FROM cases_tb WHERE country_name=?", (country_dropdown,))
row = curr.fetchone()
conn.commit()

# Closes database connection
conn.close()

# Constants
POPULATION_SIZE = row[3]
BETA = 2.2
SIGMA = 1 / 5.2
GAMMA = 1 / 2.3
REPRODUCTION_NUMBER = BETA / GAMMA

period = []
time = [0]
restrictions = []

# Stores the intervals selected by the user
for user_interval in range(len(duration)):
    period.append(int(duration[user_interval].get()))

# Time keeps track of the cumulative intervals
time += list(accumulate(period))

# NumPy array containing all x-axis values for SEIR model plot with 0.5 day intervals
total_time = np.linspace(0, time[-1], time[-1]*2 + 1)

infected_population = []

# Stores the constants to adjust the contact rate for each interval
for contact in range(len(state)):
    if state[contact].get() == "Lockdown":
        restrictions.append(0.26)
    elif state[contact].get() == "Vacation":
        restrictions.append(0.46)
    elif state[contact].get() == "School closure":
        restrictions.append(0.8)
    else:
        restrictions.append(1)

# Initial conditions for the selected country
susceptible_initial = POPULATION_SIZE - row[2] - row[1]
exposed_initial = 0
infected_initial = row[2]
recovered_initial = row[1]

# Two plots are created in the horizontal direction
fig, ax = plt.subplots(1, 2)

# Provides a solution for the system of differential equations for each interval selected by the user
for graph in range(len(period)):

    # Adjusts the contact rate for each interval
    beta = BETA * restrictions[graph]

    # Stores values of time along the x-axis
    duration = np.linspace(time[graph], time[graph+1], period[graph] * 2 + 1)
    
    # Stores values of population along the y-axis
    solution = odeint(differential, (susceptible_initial, exposed_initial, infected_initial, recovered_initial),
                      duration, args=(beta, SIGMA, GAMMA, POPULATION_SIZE))

    # New initial conditions for next interval
    susceptible_initial = solution[period[graph] * 2, 0]
    exposed_initial = solution[period[graph] * 2, 1]
    infected_initial = solution[period[graph] * 2, 2]
    recovered_initial = solution[period[graph] * 2, 3]

    # Stores all population values from differential equations solver
    # All values are collected for the first interval
    # For subsequent intervals the repeated value is avoided
    if graph == 0:
        for infected_solution in solution[:, 2]:
            infected_population.append(infected_solution)
    else:
        for infected_solution_2 in solution[1:, 2]:
            infected_population.append(infected_solution_2)

    # Plots the solutions to the system of differential equations
    if graph == 0:
        ax[0].plot(duration, solution[:, 0], 'r', label='Susceptible')
        ax[0].plot(duration, solution[:, 1], 'g', label='Exposed')
        ax[0].plot(duration, solution[:, 2], 'b', label='Infected')
        ax[0].plot(duration, solution[:, 3], 'y', label='Recovered')

    # Prevents the repetition of labels while plotting
    else:
        ax[0].plot(duration, solution[:, 0], 'r')
        ax[0].plot(duration, solution[:, 1], 'g')
        ax[0].plot(duration, solution[:, 2], 'b')
        ax[0].plot(duration, solution[:, 3], 'y')

# Provides the R0 and Rt values in the console
print("Basic reproduction number (R0) = " + str(REPRODUCTION_NUMBER))
print("Effective reproduction number (Rt) = " + str("%.3f" % (REPRODUCTION_NUMBER * solution[period[-1] * 2, 0] / POPULATION_SIZE)))

# Finds the maximum active cases and the date at which it would occur
maximum_active_y = max(infected_population)
index = infected_population.index(maximum_active_y)
maximum_active_x = total_time[index]

# Sets the domain and range for the SEIR model plot
ax[0].set_xlim(0, time[-1])
ax[0].set_ylim(0, POPULATION_SIZE + POPULATION_SIZE*0.01)

# Creates a legend to indicate susceptible, expected, infected, and recovered populations
ax[0].legend(loc='best')

# Labels axes
ax[0].set_xlabel('Time (days)')
ax[0].set_ylabel('Population')

# Creates grid to ease approximations for users
ax[0].grid()

# Creates a zoomed plot to show the maximum infected cases
try:
    
    # Creates a plot with values to the left and right of the maximum
    # Occurs only if the maximum does not lie on an edge of the SEIR model plot
    ax[1].plot(total_time[int(maximum_active_x*2):int((maximum_active_x + 5)*2)], 
        infected_population[int(maximum_active_x*2):int((maximum_active_x + 5)*2)], 'b')
    ax[1].plot(total_time[int((maximum_active_x - 5)*2):int(maximum_active_x*2 + 1)], 
        infected_population[int((maximum_active_x - 5)*2):int(maximum_active_x*2 + 1)], 'b')

except:
    try:
        
        # Plot created if the maximum lies on the left edge of the SEIR model plot
        ax[1].plot(total_time[int(maximum_active_x*2):int((maximum_active_x + 5)*2)], 
            infected_population[int(maximum_active_x*2):int((maximum_active_x + 5)*2)], 'b')
    
    except:
        try:
            
            # Plot created if the maximum lies on the right edge of the SEIR model plot
            ax[1].plot(total_time[int((maximum_active_x - 5)*2):int(maximum_active_x*2 + 1)], 
                infected_population[int((maximum_active_x - 5)*2):int(maximum_active_x*2 + 1)], 'b')
        
        except:
            
            # Plot created if the left and right of the maximum do not exist
            ax[1].plot(total_time[int(maximum_active_x*2):int(maximum_active_x*2 + 1)], 
                infected_population[int(maximum_active_x*2):int(maximum_active_x*2 + 1)], 'b')

# Sets a limit for the values of the y-axis to zoom in on maximum of infected cases
ax[1].set_ylim(0, maximum_active_y + max(maximum_active_y*0.1, 10000))

# Labels axes to match previous plot
ax[1].set_xlabel('Time (days)')
ax[1].set_ylabel('Population')

# Creates arrow pointing to the maximum of the infected cases plot
ax[1].annotate("max infected cases = " + str(int(maximum_active_y)), xy=(maximum_active_x, maximum_active_y), 
    xytext=(maximum_active_x - 3, maximum_active_y + max(9000, maximum_active_y*0.06)),
    arrowprops=dict(arrowstyle="-", connectionstyle="arc3")
)

# Legend makes it easy to compare both plots
ax[1].legend(['Infected'], loc='best')

# Eases estimation for users with a grid
ax[1].grid()

# Attempts to show the plots with fullscreen
try:
    plt.get_current_fig_manager().window.state('zoomed')

# If fullscreen fails, settle for 11x6 inch figure
except:
    fig.set_size_inches(11, 6)

# Reduces white space
plt.tight_layout()

plt.show()
