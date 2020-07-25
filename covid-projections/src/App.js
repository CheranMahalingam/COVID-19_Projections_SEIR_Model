import React from "react";
import Home from "./Views/Home";
import Method from "./Views/Method";
import Projections from "./Views/Projections";
import Results from "./Views/Results";
import Instruction from "./Views/Instruction";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route path="/projections">
            <Projections />
          </Route>
          <Route path="/instructions">
            <Instruction />
          </Route>
          <Route path="/method">
            <Method />
          </Route>
          <Route path="/results">
            <Results />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
