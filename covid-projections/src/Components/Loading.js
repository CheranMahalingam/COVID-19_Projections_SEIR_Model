import React from "react";
import Loader from "react-loader-spinner";

function Loading() {
  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{ height: 600 }}
    >
      <Loader type="ThreeDots" color="#00BFFF" height="100" width="100" />
    </div>
  );
}

export default Loading;
