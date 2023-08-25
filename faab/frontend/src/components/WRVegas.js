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
import Paper from '@material-ui/core/Paper';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import customtheme from "../style/theme";
function themeFunction(){

}



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
                                <Box
                                sx={{
                                    bgcolor: 'background.paper',
                                    pt: 8,
                                    pb: 6,
                                }}
                                >
                                    <Container maxWidth="sm">
                                        <Typography
                                        component="h1"
                                        variant="h2"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div style = {{textDecoration: 'underline'}} >
                                        2023 Draft Rankings</div>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                        <div>Crowd Sourced Rankings</div><br></br>
                                        </Typography>

                                        <Box
                                          component="img"
                                          sx={{
                            

                                          }}
                                          alt="WRs ADP vs Vegas Projections."
                                          src="../static/images/wr_by_vegas_odds.jpg"
                                        />
                                    </Container>
                                </Box>
                                <Box>
                                    <Container sx={{ py: 8 }} maxWidth="md">

                                        <Grid container spacing={4}>


                                        </Grid>
                                    </Container>        
                                </Box>      
                            </Container>
                        )  }
                </main>

                </ThemeProvider>
            </html>
        );
        
    }
}