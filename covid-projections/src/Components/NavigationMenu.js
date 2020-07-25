import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function NavigationMenu(props) {
  const [screenHeight, setScreenHeight] = useState();
  useEffect(() => {
    setScreenHeight({
      height: window.document.documentElement.offsetHeight,
    });
  }, []);

  return (
    <ul
      className="nav flex-column list-unstyled position-fixed bg-dark container-fluid min-vh-100 avoid-navbar"
      style={screenHeight}
    >
      <li className="nav-item mt-5 ml-3 mb-4">
        <Link to="/" onClick={props.closeMenu}>
          Home
        </Link>
      </li>
      <li className="nav-item ml-3 mb-4 mt-3">
        <Link to="/instructions" onClick={props.closeMenu}>
          Instructions
        </Link>
      </li>
      <li className="nav-item ml-3 mb-4 mt-3">
        <Link to="/projections" onClick={props.closeMenu}>
          Projections
        </Link>
      </li>
      <li className="nav-item ml-3 mb-4 mt-3">
        <Link to="/method" onClick={props.closeMenu}>
          Method
        </Link>
      </li>
    </ul>
  );
}

export default NavigationMenu;
