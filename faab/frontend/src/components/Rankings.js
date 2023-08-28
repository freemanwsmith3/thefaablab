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
import { slide as Menu } from 'react-burger-menu'
import CircularProgress from '@material-ui/core/CircularProgress';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';

import customtheme from "../style/theme";
function themeFunction(){
   
}
export default class Rankings extends Component {
    
    showSettings (event) {
        event.preventDefault();

      }
    
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
            votedLow: false,
            loading: true,
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
        this.handleOpen = this.handleOpen.bind(this)
        this.handleClose = this.handleClose.bind(this)
        this.handleVotedLow = this.handleVotedLow.bind(this)
        this.handleVotedMid = this.handleVotedMid.bind(this)
        this.handleVotedTop = this.handleVotedTop.bind(this)
    }

    async componentDidMount(){
        fetch('/api/get-voting'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {
            this.setState({

                votingPlayersTop: data.slice(0,3),
                votingPlayersMid: data.slice(3,6),
                votingPlayersLow: data.slice(6,9)
                // mean_values: data.mean_values,
                // mode_values: data.mode_values,
                // median_values: data.median_values,
                // num_bids: data.num_bids,
                // visibleTargets: data.visibleTargets
            });
            console.log(this.state.votingPlayersTop)
            console.log(this.state.votingPlayersMid)
            console.log(this.state.votingPlayersLow)
        });
        fetch('/api/get-rankings'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {
            this.setState({

                currentRankings: data,
                loading: false
                // mean_values: data.mean_values,
                // mode_values: data.mode_values,
                // median_values: data.median_values,
                // num_bids: data.num_bids,
                // visibleTargets: data.visibleTargets
            });
        });
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

    handleVotedTop = (index) => {
        console.log(index)

        
        
        let newRank = this.state.votingPlayersTop[index].avg_rank -(index)
        let playerid = this.state.votingPlayersTop[index].id
        
        const submitVotes = {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                week: parseInt(this.weekNumber), 
                rank: newRank,
                playerid: playerid
            }),

        };

        fetch("/api/vote", submitVotes)
            .then((response) => response.json())
            .then((data) => console.log(data))
            .then(this.reloadPage);
    
        
        this.setState({
            votedTop: true,
        })
    }

    handleVotedMid = (index) => {
        console.log(index)

        
        let newRank = this.state.votingPlayersMid[index].avg_rank -(index)
        let playerid = this.state.votingPlayersMid[index].id
        
        const submitVotes = {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                week: parseInt(this.weekNumber), 
                rank: newRank,
                playerid: playerid
            }),

        };

        fetch("/api/vote", submitVotes)
            .then((response) => response.json())
            .then((data) => console.log(data))
            .then(this.reloadPage);
    
        
        this.setState({
            votedMid: true,
        })
    }

    handleVotedLow = (index) => {
        console.log(index)

        
        let newRank = this.state.votingPlayersLow[index].avg_rank -(index )
        let playerid = this.state.votingPlayersLow[index].id
        
        const submitVotes = {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                week: parseInt(this.weekNumber), 
                rank: newRank,
                playerid: playerid
            }),

        };

        fetch("/api/vote", submitVotes)
            .then((response) => response.json())
            .then((data) => console.log(data))
            .then(this.reloadPage);
    
        
        this.setState({
            votedLow: true,
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
                        <Toolbar>
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
                {
                    this.state.votedTop ? (
                        this.state.votedMid ? (
                            this.state.votedLow ? (
                                this.state.openPop ? (
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
                                    You just voted for three rankings adjustments for the half PPR season long draft rankings
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    The rankings you see below is the consensus based off user rankings
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    You also see the comparison to ADP (Average Draft Position) to show the sentiment of fantasy nerds versus the average of casual players
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    Each week in the season this will be updated and compared to Expert Consensus Rankings
                                    </Typography>
                                    </li>
                                    {/* <li>
                                    <Typography component='h5' variant='h5'>
                                    Zero % bids will not be stored, but will allow you to see the data 
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    After submission, the consensus data will be shown to you
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    Use the crowdsourced data to get an edge in your league
                                    </Typography>
                                    </li> */}
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
                                        <a href=" http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/draftdashboard300x250.gif" width="300" height="250"/></a>
                                        </Typography>
                                        <Typography align="center">
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={this.handleOpen}>
                                            How it works
                                            </Button>
                                        </Typography>
                                        <TableContainer component={Paper}>
                                        <Table  aria-label="simple table">
                                          <TableHead>
                                            <TableRow>
                                              <TableCell>Rank</TableCell>
                                              <TableCell>Player</TableCell>
                                              {/* <TableCell>Team</TableCell>
                                              <TableCell>Position</TableCell>  */}
                                              <TableCell>User Consensus (vs. ADP)</TableCell>   
                                              {/* <TableCell>Positional Rank</TableCell> */}
                                            </TableRow>
                                          </TableHead>
                                          <TableBody>
                                            {/* <TableRow>
                                                <TableCell>dsafdsa</TableCell>
                                                <TableCell>ddsdfasd</TableCell>
                                                <TableCell>asdfd</TableCell>
                                            </TableRow> */}
                                            
                                            {this.state.currentRankings.map((row,index) => (
                                               
                                                <TableRow key={index}>
                                                    <TableCell>{index+1}</TableCell>
                                                    <TableCell>{row.name} <br></br> ({row.position_type} | {row.abbreviation})</TableCell>
                                                    {/* <REPLACE 5 WITH THE ADP THAT YOU ADD TO MODELS*/}
                                                    {row.avg_rank<row.ecr && 
                                                    <TableCell>{row.avg_rank.toFixed(1)}  <span style={{color: "red"}}>({(row.avg_rank.toFixed(1)-row.ecr).toFixed(1)})</span></TableCell>}
                                                    {row.avg_rank>=row.ecr && 
                                                    <TableCell>{row.avg_rank.toFixed(1)}  <span style={{color: "green"}}>(+{(row.ecr).toFixed(1)-row.avg_rank.toFixed(1)})</span></TableCell>}
                                                </TableRow>)
                                            )}
                                        </TableBody>
                                        </Table>
                                      </TableContainer>
                                    </Container>
                                </Box>
                                <Box>
                                    <Container sx={{ py: 8 }} maxWidth="md">
                                                                            

                                    {/* End hero unit */}
                                        <Grid container spacing={4}>


                                        </Grid>
                                    </Container>        
                                </Box>      
                            </Container>
                        )  ):(                            <Container maxWidth="md">
                        <Box
                        sx={{
                            bgcolor: 'background.paper',
                            pt: 8,
                            pb: 6,
                        }}>
                             <Typography
                                        component="h3"
                                        variant="h4"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        
                                        ><div >To view the crowdsourced rankings, choose who you'd draft higher (half PPR)</div>
                                        </Typography>
                            
                            <Typography align="center">
                            {this.state.votingPlayersLow.map((row,index) => (
                                         <Button 
                                         variant="contained" 
                                         color="primary" 
                                         onClick={() => this.handleVotedLow(index)}>
                                         <h4><span style={{fontSize: 'large'}}>{row.name}</span> <br></br>{row.position_type} |  {row.abbreviation}</h4>
                                         </Button>
                                            ))}
                                     <Typography
                                        component="h4"
                                        variant="h5"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div >
                                        (3/3)</div>
                                        </Typography>
                                  
                                </Typography>
                        </Box>
                    </Container>)):
                    (<Container maxWidth="md">
                        <Box
                        sx={{
                            bgcolor: 'background.paper',
                            pt: 8,
                            pb: 6,
                        }}>
                             <Typography
                                        component="h3"
                                        variant="h4"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div >To view the crowdsourced rankings, choose who you'd draft higher (half ppr)</div>
                                        </Typography>

                            
                            <Typography align="center">
                            {this.state.votingPlayersMid.map((row,index) => (
                                    <Button 
                                    variant="contained" 
                                    color="primary" 
                                    onClick={() => this.handleVotedMid(index)}>
                                    <h4><span style={{fontSize: 'large'}}>{row.name}</span> <br></br>{row.position_type} |  {row.abbreviation}</h4>
                                    </Button>
                                            ))}
                                    <Typography
                                        component="h4"
                                        variant="h5"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div >
                                        (2/3)</div>
                                        </Typography>
                                  
                                </Typography>
                        </Box>
                    </Container>)):(                            
                    <Container maxWidth="md">
                        <Box
                        sx={{
                            bgcolor: 'background.paper',
                            pt: 8,
                            pb: 6,
                        }}>
                             <Typography
                                        
                                        component="h3"
                                        variant="h4"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div >To view the crowdsourced rankings, choose who you'd draft higher (half ppr)</div>
                                        </Typography>
                       
                            <Typography align="center">
                            {this.state.loading ? (<CircularProgress /> ):(
                            this.state.votingPlayersTop.map((row,index) => (
                                        <Button 
                                        variant="contained" 
                                        color="primary" 
                                        onClick={() => this.handleVotedTop(index)}>
                                        <h4><span style={{fontSize: 'large'}}>{row.name}</span> <br></br>{row.position_type} |  {row.abbreviation}</h4>
                                        </Button>
                                            )))}
                                          <Typography
                                        component="h4"
                                        variant="h5"
                                        align="center"
                                        color="text.primary"
                                        gutterBottom
                                        ><div >
                                        (1/3)</div>
                                        </Typography>
                            
                                  
                                </Typography>
                        </Box>
                    </Container>)}

                   

                </main>

                </ThemeProvider>
            </html>
        );
        
    }
}