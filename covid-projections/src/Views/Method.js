import React from "react";
import Navigation from "../Components/Navigation";
import Equations from "../Images/SEIR_differential_equations.png";
import Diagram from "../Images/SEIR_diagram.png";

function Method() {
  return (
    <div className="bg-white">
      <Navigation />
      <br />
      <br />
      <br />
      <h2 className="ml-3">The SEIR model</h2>
      <blockquote className="ml-5 w-75">
        This application makes projections by separating the population into
        those who are susceptible, exposed, infectious, and recovered. The
        susceptible population includes people who can become infecteds. Those
        who are exposed are in a transition state where they have been infected,
        however, they have yet to become infectious. These people then enter the
        infectious state where they are contagious. Once they recover they
        develop immunity to the disease and they are placed in the recovered
        population [3].
      </blockquote>
      <br />
      <blockquote className="ml-5 w-75">
        In order to estimate the number of people that exist in each group at a
        given time we have to examine the initial size of each group and their
        respective inflows and outflows as shown in the figure below. The
        transfer of people from the susceptible group to the exposed group
        relies on the contact rate and transmission probability given by &beta;.
        The transfer of people from the exposed group to the infected group
        depends on the incubation period given by &sigma; and the transfer to
        the recovered group depends on the recovery period given by &gamma;.
      </blockquote>
      <img
        src={Diagram}
        alt="SEIR diagram"
        className="w-50 width-adjust mb-3 mt-2"
      />
      <blockquote className="ml-5 w-75">
        Therefore, the rate at which people leave or enter each group can be
        modelled by a series of differential equations. Given the initial size
        of each population we can evaluate the final size of each group by
        solving the following system of differential equations.
      </blockquote>
      <br />
      <img src={Equations} alt="SEIR equations" className="width-adjust" />
      <h2 className="ml-3">How information is gathered</h2>
      <blockquote className="ml-5 w-75">
        The application gets real-time data regarding active cases, recoveries,
        and population for individual countries by webscraping from the
        Worldometers website. This data provides the initial conditions used in
        the SEIR model. Data for the constants used in the SEIR model
        differential equations were taken from a report made by WHO and a study
        on dynamic intervention strategies [1, 2].
      </blockquote>
      <blockquote className="ml-5 w-75">
        The application also takes the restrictions put in place by reducing the
        contact rate accordingly. A study revealed that lockdown was the most
        effective, reducing the contact rate by 74% [2]. During vacation periods
        where students are out of school and a large portion of people are not
        working, the contact rate is reduced by 54%. Finally, with school
        closures the contact rate is reduced by only 20% due to how school
        social contacts can be shifted to non-school sites [4].
      </blockquote>
      <h2 className="ml-3">Additional reading</h2>
      <ol className="ml-3">
        <li>
          <a href="https://www.who.int/bulletin/online_first/20-255695.pdf">
            CoronaTracker: World-wide COVID-19 Outbreak Data Analysis and
            Prediction
          </a>
        </li>
        <li>
          <a href="https://link.springer.com/article/10.1007/s10654-020-00649-w">
            Dynamic interventions to control COVID-19 pandemic: a multivariate
            prediction modelling study comparing 16 worldwide countries
          </a>
        </li>
        <li>
          <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7270519/">
            Compartmental Models of the COVID-19 Pandemic for Physicians and
            Physician-Scientists
          </a>
        </li>
        <li>
          <a href="https://www.thelancet.com/journals/lanchi/article/PIIS2352-4642(20)30095-X/fulltext">
            School closure and management practices during coronavirus outbreaks
            including COVID-19: a rapid systematic review
          </a>
        </li>
      </ol>
    </div>
  );
}

export default Method;
