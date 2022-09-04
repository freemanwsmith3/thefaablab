import React, { Component } from "react";
import { render } from "react-dom";
import BidPlayer from "./BidPlayer";
import HomePage from "./HomePage";
import ShowData from "./ShowData";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="center">
        <HomePage />
      </div>
      ); 
    }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);