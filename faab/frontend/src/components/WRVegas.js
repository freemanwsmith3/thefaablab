import React, { Component} from "react";
import ShowData from "./ShowData";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import BidPlayer from "./BidPlayer";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import CssBaseline from '@material-ui/core/CssBaseline';
import Button from '@material-ui/core/Button';
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import Card from '@material-ui/core/Card';
import { makeStyles, ThemeProvider } from '@material-ui/core/styles';
import customtheme from "../style/theme";
function themeFunction(){

}
const useStyles = makeStyles({
  responsiveImage: {
    maxWidth: '100%',
    height: 'auto',
    display: 'block'
  }
});


export default class WRVegas extends Component {
    

    constructor(props) {
        super(props);
        this.theme = themeFunction();
        this.state = {
            votingPlayersTop: [],
            votingPlayersMid: [],
            votingPlayersLow: [],
            currentRankings : [],
            openPop: false,
            votedTop: false,
            votedMid: false,
            votedLow: false
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
        this.handleOpen = this.handleOpen.bind(this)
        this.handleClose = this.handleClose.bind(this)

    }

  
    handleOpen(e){

        this.setState({
            openPop: true,

        })
    }

    handleClose(e){

        this.setState({
            openPop: false,
        })
    }


    render(){
        const {classes} = this.props;
        
        return(
            <html >
                <ThemeProvider theme={customtheme}> 
                <CssBaseline />
                <header>
                    <AppBar position="relative">
                        <Toolbar     sx={{
                                    fill: 'green',
                                    pt: 8,
                                    pb: 6,
                                }}>
                        {/* <SportsFootballOutlinedIcon sx={{ mr: 2 }} /> */}
                        
                        <Typography variant="h3" color="inherit" noWrap>
                            FAABLab
                        </Typography>
                        {/* <ClickAwayListener onClickAway={this.handleClickAway}>
                            <Box sx={{ position: 'relative' }}>
                                <button type="button" onClick={this.handleClick}>
                                Open menu dropdown
                                </button>
                                {open ? (
                                <Box >
                                    Click me, I will stay visible until you click outside.
                                </Box>
                                ) : null}
                            </Box>
                        </ClickAwayListener> */}
                        </Toolbar>
                    </AppBar>
                </header>
                <main id="app">
                {this.state.openPop ? (
                            <Container maxWidth="md">
                                <Box
                                sx={{
                                    bgcolor: 'background.paper',
                                    pt: 8,
                                    pb: 6,
                                }}>
                                    <Typography component='h5' variant='h5'>
                                        How it works:
                                    </Typography>
                                    <ul><li>
                                    <Typography component='h5' variant='h5'>
                                    You just voted for three rankings adjustments for this weke
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    The rankings you see below is the consensus based off user rankings
                                    </Typography>
                                    </li>
                                    </ul>
                                    <Typography align="center">
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={this.handleClose}>
                                            Close
                                            </Button>
                                        </Typography>
                                </Box>
                            </Container>
                        ) : (
                            <Container>
                    
                                
                                    <Container maxWidth="sm" >
                            
                                        <Typography align="center" component='h5' variant='h5' >
                                        <div>
                                                    <h3>Vegas WR Lines vs. ADP</h3>
                                                    <p>The chart presented offers an in-depth analysis of fantasy football wide receivers. Rankings are determined based on their projected season long fantasy outputs, which have been derived from Las Vegas lines predicting receiving yards and touchdowns for the upcoming season.</p>
                                                    <p>These projections give us a predictive framework to assess a player's potential performance. The chart compares these projections against the average draft position (ADP) for wide receivers in standard fantasy football leagues. This comparative view allows fantasy managers to discern where the general consensus might be underestimating (or overestimating) a player's true value.</p>
                                                    <p>By capitalizing on these market inefficiencies and making well-informed drafting decisions, fantasy football managers can gain a significant edge over their competition, optimizing their roster for success throughout the season.</p>
                                                </div>

                                        </Typography>
                                                                                
                                        <Card 
                                            sx={{  height: '100%', display: 'block', flexDirection: 'column'}} >
                                                           <CardMedia
                                                component="img"
                                                sx={{
                                                // 16:9
                                                pt: '56.25%',
                                                }}
                                                image="../static/images/wr_by_vegas_odds.jpg"
                                                alt="WRs ADP vs Vegas Projections."
                />                 

                                         
                                            </Card>

                                    </Container>

                            </Container>
                        )  }
                </main>

                </ThemeProvider>
            </html>
        );
        
    }
}
