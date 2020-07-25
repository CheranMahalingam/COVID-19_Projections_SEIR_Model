# Modelling the Spread of COVID-19 using an SEIR Model
# Instructions
1. Open the api.py file located in the api directory and change the 'path' variable to the directory
   in which the scrapy.cfg is located

   ` path = "********/COVID-19_Projections_SEIR_Model/api/Covid_Webscraper" `

2. Open the terminal and cd into the covid-projections directory

   ` cd *****/COVID-19_Projections_SEIR_Model/covid-projections `

3. To run the flask backend as a windows user use,

   ` npm run start-api `
   For Mac and Linux users use,

   ` npm run start-api-2 `

4. Open a new terminal and cd into the covid-projections directory

   ` cd *****/COVID-19_Projections_SEIR_Model/covid-projections `

5. To run the web application use,

   ` npm start `

# SEIR Model
The model splits the population into four groups. Susceptible (people who are not immune 
to infection), Exposed (people who have been infected but are yet to become infectious), 
Infected (people who can spread the disease), Recovered (people who are immune).
The population of each group can be approximated using the following differential 
equations:

<p align="center">
  <img src="images/SEIR_differential_equations.png">
</p>

# Definitions
Basic Reproduction Number (R0): Measures transmission potential by representing how many 
additional cases are caused by one individual when no restrictions are placed. When R0 > 
1 the disease will be able to propagate and measures must be placed to slow down its 
spread.

Effective Reproduction Number (Rt): Measures transmission potential when there are 
individuals who are immune or intervention measures in place to reduce the spread. Once 
  Rt < 1 the disease will struggle to propagate.
