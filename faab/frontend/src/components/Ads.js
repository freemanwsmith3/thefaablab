import React, { Component } from "react";
import Box from "@material-ui/core/Box";
import Container from "@material-ui/core/Container";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Card from '@material-ui/core//Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import DetailedHistogram from "./DetailedHistogram";
import { borders } from '@material-ui/system';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import customtheme from "../style/ads";
function themeFunction(){
}

export default class Ads extends Component {
    constructor(props) {
        super(props);
        this.adIndex = this.props.adIndex;

    }


    // }


    render() {
        return (
            <ThemeProvider theme={customtheme}> 
            <Grid  xs={12} sm={6} md={4 } >    
           <Card 
            sx={{  height: '100%', align: 'center', display: 'fled', flexDirection: 'column'}} > 
            {this.adIndex ===2  && 
            <a href=" http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/draftdashboard300x250.gif" alt="draft-dashboard" width="100%" height="100%" /></a>
            }
            {this.adIndex ===5 && 
            <a href='https://www.dailyfantasynerd.com?afmc=ba'><img src='https://leaddyno-client-images.s3.amazonaws.com/71204ad8ccb61f89f443611d24ec951b101516a9/9b35e83b1d0115d035f536cfa5bbddfa99c951e4_DFN-MLB-300x250.png' width="100%" height="100%" /></a>
            }
            {this.adIndex === 9 && 
            <a href=" http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/draftdashboard300x250.gif" alt="draft-dashboard" width="100%" height="100%" /></a>
            }
            {this.adIndex === 12 && 
            <a href='https://www.dailyfantasynerd.com?afmc=ba'><img src='https://leaddyno-client-images.s3.amazonaws.com/71204ad8ccb61f89f443611d24ec951b101516a9/9b35e83b1d0115d035f536cfa5bbddfa99c951e4_DFN-MLB-300x250.png' width="100%" height="100%" /></a>
            }
            </Card>
            <Card 
            sx={{  height: '100%', align: 'center', display: 'fled', flexDirection: 'column'}} > 
            {this.adIndex ===2 && 
            <a href='https://www.dailyfantasynerd.com?afmc=ba'><img src='https://leaddyno-client-images.s3.amazonaws.com/71204ad8ccb61f89f443611d24ec951b101516a9/0ec7cd0a590b758c96e947630563cfbbbbb6f049_DFN-NFL-300x250.png'  alt="draft-dashboard"  width="100%" height="100%" /></a>
            }
            {this.adIndex ===5 && 
            <a href="http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/creative300anim.gif"  alt="draft-dashboard"  width="100%" height="100%"/></a>
            }
            {this.adIndex === 9 && 
            <a href='https://www.dailyfantasynerd.com?afmc=ba'><img src='https://leaddyno-client-images.s3.amazonaws.com/71204ad8ccb61f89f443611d24ec951b101516a9/0ec7cd0a590b758c96e947630563cfbbbbb6f049_DFN-NFL-300x250.png' width="100%" height="100%" /></a>
            }
            {this.adIndex === 12 && 
            <a href="http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/creative300anim.gif" width="100%" height="100%"/></a>
            }
           
            </Card></Grid>
            </ThemeProvider>
        );
      }
    }