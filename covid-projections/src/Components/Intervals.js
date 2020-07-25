import React from "react";

function Intervals(props) {
  function handleRestrictionChange(event) {
    return props.onRestrictionUpdate(event.target.value, props.count);
  }

  function handleIntervalChange(event) {
    return props.onIntervalUpdate(event.target.value, props.count);
  }

  return (
    <label className="ml-4 mt-2 mb-3 row">
      <h6 className="mt-1">Interval {props.count.id}:&nbsp;</h6>
      <input
        className="ml-1"
        type="number"
        min="0"
        id="length"
        onChange={handleIntervalChange}
      />
      <select
        className="ml-1"
        onChange={handleRestrictionChange}
        id="restriction"
        defaultValue="None"
      >
        <option key="1" value="Lockdown">
          Lockdown
        </option>
        <option key="2" value="Vacation">
          Vacation
        </option>
        <option key="3" value="School closure">
          School closure
        </option>
        <option key="4" value="None">
          None
        </option>
      </select>
      <br />
    </label>
  );
}

export default Intervals;
