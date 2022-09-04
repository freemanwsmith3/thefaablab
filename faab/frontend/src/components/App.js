import React, { Component } from "react";
import { render } from "react-dom";
import BidPlayerPage from "./BidPlayerPage";
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <BidPlayerPage />
      </div>
      ); 
    }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);