import React, { useState } from "react";
import { useTransition, animated } from "react-spring";
import NavigationMenu from "./NavigationMenu";
import menu from "../Images/menu.svg";

function Navigation(props) {
  const [showMenu, setShowMenu] = useState(false);
  const transitions = useTransition(showMenu, null, {
    from: { position: "relative", opacity: 0 },
    enter: { opacity: 1 },
    leave: { opacity: 0 },
  });
  const menuTransitions = useTransition(showMenu, null, {
    from: { opacity: 0, transform: "translateX(100%)" },
    enter: { opacity: 1, transform: "translateX(0%)" },
    leave: { opacity: 0, transform: "translateX(100%)" },
  });

  function handleGraph() {
    setShowMenu(!showMenu);
    if (props.closeGraph) {
      return props.closeGraph();
    }
  }

  return (
    <div>
      <div className="bg-dark navbar fixed-top row" style={{ height: 50 }}>
        <img
          src={menu}
          alt="Menu Btn"
          className="mt-1 ml-3 menu-style"
          onClick={handleGraph}
        />
        <h6 className="text-white menu-name">Menu</h6>
      </div>
      {transitions.map(({ item, key, props }) => (
        <animated.div
          key={key}
          style={props}
          onClick={() => setShowMenu(false)}
        ></animated.div>
      ))}
      {menuTransitions.map(
        ({ item, key, props }) =>
          item && (
            <animated.div key={key} style={props}>
              <NavigationMenu closeMenu={() => setShowMenu(false)} />
            </animated.div>
          )
      )}
    </div>
  );
}

export default Navigation;
