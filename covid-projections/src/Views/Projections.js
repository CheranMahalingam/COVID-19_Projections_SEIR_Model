import React, { useState, useEffect } from "react";
import axios from "axios";
import Intervals from "../Components/Intervals";
import Navigation from "../Components/Navigation";
import Loading from "../Components/Loading";
import ReactTooltip from "react-tooltip";
import { Redirect } from "react-router";

function Projections() {
  const [selectedInterval, setSelectedInterval] = useState([
    {
      id: 1,
      length: 0,
      restriction: "None",
    },
  ]);
  const [country, setCountry] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [redirect, setRedirect] = useState(false);
  const [time, setTime] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://localhost:5000/country").then((res) => {
      const country = res.data;
      let country_list = [{ id: 0, name: "" }];
      let i = 0;
      let flag = true;
      while (flag) {
        if (country[i]) {
          country_list = country_list.concat({
            id: i + 1,
            name: country[i],
          });
          i++;
        } else {
          break;
        }
      }
      setLoading(false);
      setCountry(country_list);
    });
  }, []);

  function handleCountry(event) {
    setSelectedCountry(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (selectedCountry !== "") {
      axios
        .post("http://localhost:5000/submit", {
          intervalData: selectedInterval,
          countryData: selectedCountry,
        })
        .then((res) => {
          setRedirect(true);
        });
    } else {
      alert("Ensure that you have selected a country");
    }
  }

  function handleInterval(newValue, key) {
    const cool = [...selectedInterval];
    const index = cool.indexOf(key);
    cool[index] = { ...key };
    cool[index].length = newValue;
    setSelectedInterval(cool);
  }

  function handleRestriction(newValue, key) {
    const cool = [...selectedInterval];
    const index = cool.indexOf(key);
    cool[index] = { ...key };
    cool[index].restriction = newValue;
    setSelectedInterval(cool);
  }

  function handleAddition() {
    const cool = [...selectedInterval];
    cool.push({
      id: selectedInterval.length + 1,
      length: 0,
      restriction: "None",
    });
    setSelectedInterval(cool);
  }

  function handleDeletion() {
    const cool = [...selectedInterval];
    cool.pop();
    setSelectedInterval(cool);
  }

  function handleScrape() {
    setLoading(true);
    axios.get("http://localhost:5000/scrape/").then((res) => {
      setTime("Data last updated: " + res.data);
      setLoading(false);
    });
  }

  if (redirect) {
    return <Redirect to="/results" />;
  }

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="bg-white">
      <Navigation />
      <br />
      <br />
      <br />
      <div className="float-right mr-5">
        <button
          data-tip
          data-for="info"
          className="btn btn-warning mr-1"
          onClick={handleScrape}
        >
          Refresh
        </button>
      </div>
      <br />
      <div className="d-flex flex-row">
        <h5 className="ml-4">Select a country:&nbsp;</h5>
        <select className="ml-1" onChange={handleCountry}>
          {country.map((country) => (
            <option key={country.id} value={country.name}>
              {country.name}
            </option>
          ))}
        </select>
      </div>
      <h5 className="ml-4 mt-5">
        Enter the duration of the interval and the restriction implemented:
      </h5>
      <button
        data-tip
        data-for="addition"
        className="btn btn-primary btn-sm ml-5 mt-2 mb-4 mr-1"
        style={{ width: 30 }}
        onClick={handleAddition}
      >
        +
      </button>
      <button
        data-tip
        data-for="delete"
        className="btn btn-danger btn-sm ml-1 mt-2 mb-4"
        style={{ width: 30 }}
        onClick={handleDeletion}
      >
        -
      </button>
      <br />
      {selectedInterval.map((interval) => (
        <Intervals
          key={interval.id}
          onIntervalUpdate={handleInterval}
          onRestrictionUpdate={handleRestriction}
          count={interval}
        />
      ))}
      <form onSubmit={handleSubmit} action="/results">
        <button className="ml-4 mt-3 btn btn-success" type="submit">
          Enter
        </button>
      </form>
      <p>{time}</p>
      <ReactTooltip id="info" place="bottom" effect="solid">
        Update case numbers
      </ReactTooltip>
      <ReactTooltip id="addition" effect="solid">
        Append an additional interval
      </ReactTooltip>
      <ReactTooltip id="delete" effect="solid">
        Remove the last interval
      </ReactTooltip>
    </div>
  );
}

export default Projections;
