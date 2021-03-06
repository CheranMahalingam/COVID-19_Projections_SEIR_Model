import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import InnerHTML from "dangerously-set-html-content";
import Loading from "../Components/Loading";
import Navigation from "../Components/Navigation";
import { useSpring, animated, config, useChain } from "react-spring";
import ReactTooltip from "react-tooltip";

function Results() {
  const [graphHTML, setGraphHTML] = useState();
  const [loading, setLoading] = useState(true);
  const [showGraph, setShowGraph] = useState(true);
  const [R0, setR0] = useState(0);
  const [Rt, setRt] = useState(0);
  const [maxActive, setMaxActive] = useState(0);
  const [susceptibleState, setSusceptibleState] = useState(0);
  const [exposedState, setExposedState] = useState(0);
  const [infectedState, setInfectedState] = useState(0);
  const [recoveredState, setRecoveredState] = useState(0);

  let graph;

  const R0Ref = useRef();
  let R0Spring = useSpring({
    number: R0,
    from: { number: 0 },
    config: config.molasses + { clamp: true },
    delay: 1000,
    ref: R0Ref,
  });

  const RtRef = useRef();
  let RtSpring = useSpring({
    number: Rt,
    from: { number: 0 },
    config: config.molasses + { clamp: true },
    delay: 2000,
    ref: RtRef,
  });

  const maxActiveRef = useRef();
  let maxActiveSpring = useSpring({
    number: maxActive,
    from: { number: 0 },
    config: config.gentle + { clamp: true },
    delay: 3000,
    ref: maxActiveRef,
  });

  const susceptibleRef = useRef();
  let susceptibleSpring = useSpring({
    number: susceptibleState,
    from: { number: 0 },
    config: config.gentle + { clamp: true },
    delay: 4000,
    ref: susceptibleRef,
  });

  const exposedRef = useRef();
  let exposedSpring = useSpring({
    number: exposedState,
    from: { number: 0 },
    config: config.gentle + { clamp: true },
    delay: 5000,
    ref: exposedRef,
  });

  const infectedRef = useRef();
  let infectedSpring = useSpring({
    number: infectedState,
    from: { number: 0 },
    config: config.gentle + { clamp: true },
    delay: 6000,
    ref: infectedRef,
  });

  const recoveredRef = useRef();
  let recoveredSpring = useSpring({
    number: recoveredState,
    from: { number: 0 },
    config: config.gentle + { clamp: true },
    delay: 7000,
    ref: recoveredRef,
  });

  useChain([
    R0Ref,
    RtRef,
    maxActiveRef,
    susceptibleRef,
    exposedRef,
    infectedRef,
    recoveredRef,
  ]);

  useEffect(() => {
    axios.get("http://localhost:5000/result").then((res) => {
      let data = res.data;
      setGraphHTML(data["graph"]);
      setR0(data["r0"]);
      setRt(data["rt"]);
      setMaxActive(data["max_active_cases"]);
      setSusceptibleState(data["susceptible_state"]);
      setExposedState(data["exposed_state"]);
      setInfectedState(data["infected_state"]);
      setRecoveredState(data["recovered_state"]);
      setLoading(false);
    });
  }, []);

  function handleGraph() {
    setShowGraph(!showGraph);
  }

  if (loading) {
    return <Loading />;
  }

  if (showGraph && !loading) {
    graph = <InnerHTML className="text-center" html={graphHTML} />;
  }

  return (
    <div className="bg-white min-vh-100">
      <Navigation closeGraph={handleGraph} />
      <br />
      <br />
      <br />
      <div className="d-flex flex-row justify-content-around stat-alignment-1 mt-5">
        <h4 data-tip data-for="R0">
          Basic Reproduction Number
        </h4>
        <h4 data-tip data-for="Rt">
          Effective Reproduction Number
        </h4>
        <h4>Maximum Active Cases</h4>
      </div>
      <div className="d-flex flex-row">
        <div className="stat-1-1">
          <animated.span data-tip data-for="R0">
            {R0Spring.number}
          </animated.span>
        </div>
        <div className="stat-1-2">
          <animated.span>{RtSpring.number}</animated.span>
        </div>
        <div className="stat-1-3">
          <animated.span>{maxActiveSpring.number}</animated.span>
        </div>
      </div>
      <br />
      <div className="d-flex flex-row justify-content-around">
        <h4>Susceptible Population</h4>
        <h4>Exposed Population</h4>
        <h4>Infectious Population</h4>
        <h4>Recovered Population</h4>
      </div>
      <div className="d-flex flex-row">
        <div className="stat-2-1">
          <animated.span>{susceptibleSpring.number}</animated.span>
        </div>
        <div className="stat-2-2">
          <animated.span>{exposedSpring.number}</animated.span>
        </div>
        <div className="stat-2-3">
          <animated.span>{infectedSpring.number}</animated.span>
        </div>
        <div className="stat-2-4">
          <animated.span>{recoveredSpring.number}</animated.span>
        </div>
      </div>
      <br />
      {graph}
      <br />
      <ReactTooltip id="R0" effect="solid">
        The average number of secondary cases generated by a single infected
        individual when intervention measures are not placed.
      </ReactTooltip>
      <ReactTooltip id="Rt" effect="solid">
        The average number of secondary cases generated by a single infected
        individual t days after intervention measures are placed.
      </ReactTooltip>
    </div>
  );
}

export default Results;
