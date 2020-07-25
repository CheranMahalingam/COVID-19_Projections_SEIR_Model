import Navigation from "../Components/Navigation";
import React from "react";
import example_plot from "../Images/SEIR_model_graph.svg";

function Home() {
  return (
    <div className="bg-white">
      <Navigation />
      <br />
      <br />
      <br />
      <h2 className="ml-3">About</h2>
      <blockquote className="ml-5 mt-3 w-75">
        This web application serves to educate people about the importance of
        social distancing during the COVID-19 outbreak through case projections
        for individual countries. Although similar applications exist, this tool
        distinguishes itself by combining real-time data with a comparison of
        how different restrictive measures can affect case numbers emphasizing
        the importance of following social distancing measures.
      </blockquote>
      <img src={example_plot} alt="plot" className="w-50 width-adjust" />
      <br />
      <br />
    </div>
  );
}

export default Home;
