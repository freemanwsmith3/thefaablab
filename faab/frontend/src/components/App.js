import React, { Component } from "react";
import { render } from "react-dom";
import BidPlayer from "./BidPlayer";
import HomePage from "./HomePage";
import Typography from "@material-ui/core/Typography";

import Box from '@material-ui/core/Box';
export default class App extends Component {
  constructor(props) {
    super(props);
  }


  render() {
    return (
      <div className="center">
        <HomePage />

      <footer>
      <Box sx={{ bgcolor: '#EAEAEA', p: 6 }} component="footer">
      <Typography variant="body2" color="text.secondary" align="center">
          Contact: faablabapp@gmail.com
          {/* {new Date().getFullYear()}
          {'.'} */}
      </Typography>
      </Box>
      </footer>
      </div>
      ); 
    }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);