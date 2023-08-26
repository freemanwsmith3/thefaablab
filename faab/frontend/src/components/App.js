import React, { Component } from "react";
import { render } from "react-dom";
import BidPlayer from "./BidPlayer";
import HomePage from "./HomePage";
import Typography from "@material-ui/core/Typography";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';

import customtheme from "../style/theme";
function themeFunction(){
}

export default class App extends Component {
  constructor(props) {
    super(props);
  }


  render() {
    return (
      
      <div className="center"  style={{backgroundColor: '#EAEAEA'}}>
        <ThemeProvider theme={customtheme}> 
        <main style={{backgroundColor: '#EAEAEA'}}>
        <HomePage />
        </main>
      <footer>
      <Box sx={{ bgcolor: '#EAEAEA', p: 6, paddingTop: '100px', marginTop: '10px' }} component="footer">
      <Typography variant="body2" align="center">
          <span style={{color:"#4F6D7A"}}>Contact: faablabapp@gmail.com</span>
          {/* {new Date().getFullYear()}
          {'.'} */}
      </Typography>
      </Box>
      </footer>
      </ThemeProvider>
      </div>
      ); 
    }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);