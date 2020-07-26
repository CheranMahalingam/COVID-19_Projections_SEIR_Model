import os
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
from matplotlib import pyplot as plt
import time
from itertools import accumulate
import mpld3
from mpld3 import plugins
from scipy.integrate import odeint
import numpy as np
import matplotlib

path = ""

matplotlib.use('Agg')


app = Flask(__name__)
cors = CORS(app)


def create_table():
    g.conn = sqlite3.connect('case_data.db')
    g.curr = g.conn.cursor()
    g.curr.execute("""DROP TABLE IF EXISTS interval_tb""")
    g.curr.execute("""CREATE TABLE interval_tb(
        country_name text,
        duration integer,
        restriction text
        )""")


@app.route("/country/", methods=['GET'])
def countries():
    os.chdir(path)
    g.conn = sqlite3.connect('case_data.db')
    g.curr = g.conn.cursor()
    g.curr.execute("SELECT country_name FROM cases_tb")
    countries = g.curr.fetchall()
    known_countries = []
    for i in range(len(countries) - 4):
        if countries[i][0] != "UK" and countries[i][0] != "Spain" and countries[i][0] != "Netherlands" and countries[i][0] != "Sweden":
            known_countries.append(countries[i][0])
    g.conn.commit()
    return jsonify(known_countries)


@app.route("/scrape/")
def scrape():
    cmd = "scrapy crawl cases"
    os.system(cmd)
    return jsonify(time.asctime())


@app.route("/submit", methods=['POST'])
def graph():
    if request.method == 'POST':
        interval_data = request.json["intervalData"]
        country_data = request.json["countryData"]
        create_table()
        for i in range(len(interval_data)):
            g.curr.execute(
                """INSERT INTO interval_tb values (?, ?, ?)""", (
                    country_data,
                    interval_data[i]['length'],
                    interval_data[i]['restriction']
                ))
        g.conn.commit()
        return jsonify(interval_data)


@app.route('/result/', methods=['GET'])
def result():
    try:
        g.conn = sqlite3.connect('case_data.db')
        g.curr = g.conn.cursor()
        g.curr.execute("SELECT country_name FROM interval_tb")
        country = g.curr.fetchone()[0]
        g.curr.execute("SELECT duration FROM interval_tb")
        period = g.curr.fetchall()
        g.curr.execute("SELECT restriction FROM interval_tb")
        restrictions = g.curr.fetchall()
        g.curr.execute(
            "SELECT * FROM cases_tb WHERE country_name=?", (country,))
        country_statistics = g.curr.fetchone()
        g.conn.commit()
        g.conn.close()

        plt.rcParams.update({'font.size': 12})

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

        POPULATION_SIZE = country_statistics[3]
        BETA = 0.956
        SIGMA = 1 / 5.2
        GAMMA = 1 / 2.3
        REPRODUCTION_NUMBER = BETA / GAMMA

        period = list(period)
        time = [0]
        restrictions = list(restrictions)
        contact_state = []

        for i in range(len(period)):
            period[i] = period[i][0]

        for i in range(len(restrictions)):
            restrictions[i] = restrictions[i][0]

        time += list(accumulate(period))

        for j in range(len(period)):
            if restrictions[j] == "Lockdown":
                contact_state.append(0.26)
            elif restrictions[j] == "Vacation":
                contact_state.append(0.46)
            elif restrictions[j] == "School closure":
                contact_state.append(0.8)
            else:
                contact_state.append(1)

        susceptible_initial = POPULATION_SIZE - \
            country_statistics[2] - country_statistics[1]
        exposed_initial = 0
        infected_initial = country_statistics[2]
        recovered_initial = country_statistics[1]

        infected_population = 0
        current_maximum = 0

        fig, ax = plt.subplots()

        for graph in range(len(period)):

            beta = BETA * contact_state[graph]

            duration = np.linspace(
                time[graph], time[graph + 1], period[graph] * 2 + 1)

            solution = odeint(differential, (susceptible_initial, exposed_initial, infected_initial, recovered_initial),
                              duration, args=(beta, SIGMA, GAMMA, POPULATION_SIZE))

            susceptible_initial = solution[period[graph]*2, 0]
            exposed_initial = solution[period[graph]*2, 1]
            infected_initial = solution[period[graph]*2, 2]
            recovered_initial = solution[period[graph]*2, 3]

            current_maximum = max(solution[:, 2])
            if current_maximum > infected_population:
                infected_population = current_maximum

            if graph == 0:
                ax.plot(duration, solution[:, 0], 'r', label='Susceptible')
                ax.plot(duration, solution[:, 1], 'g', label='Exposed')
                ax.plot(duration, solution[:, 2], 'b', label='Infectious')
                ax.plot(duration, solution[:, 3], 'y', label='Recovered')

            else:
                ax.plot(duration, solution[:, 0], 'r')
                ax.plot(duration, solution[:, 1], 'g')
                ax.plot(duration, solution[:, 2], 'b')
                ax.plot(duration, solution[:, 3], 'y')

        ax.set_xlim(0, time[-1])
        ax.set_ylim(0, POPULATION_SIZE + POPULATION_SIZE*0.01)

        ax.legend(loc='best')

        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Population', rotation='horizontal')

        fig.set_size_inches(8, 6)
        ax.yaxis.set_label_coords(-0.1, 1.02)

        plugins.clear(fig)
        plugins.connect(fig, plugins.Reset())
        plugins.connect(fig, plugins.BoxZoom(enabled=True))
        plugins.connect(fig, plugins.Zoom())

        seir_graph = mpld3.fig_to_html(fig)
        plt.close()

        effective_reproduction_number = REPRODUCTION_NUMBER * \
            susceptible_initial/POPULATION_SIZE
        effective_reproduction_number = float(
            "{:0.3f}".format(effective_reproduction_number))

        return {'graph': seir_graph, 'r0': REPRODUCTION_NUMBER, 'rt': effective_reproduction_number,
                'susceptible_state': int(susceptible_initial), 'exposed_state': int(exposed_initial), 'infected_state': int(infected_initial),
                'recovered_state': int(recovered_initial), 'max_active_cases': int(infected_population)}
    except:
        return jsonify(0)


if __name__ == '__main__':
    app.run()
