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
import customtheme from "../style/weeklytheme";


export default class WeeklyRankings extends Component {
    
    showSettings (event) {
        event.preventDefault();

      }
    
    constructor(props) {
        super(props);
        this.state = {
            votingQBs: [],
            votingWRS: [],
            votingRBs: [],
            votingTEs: [],
            currentRankings : [],
            rankingQBs: [],
            rankingWRs: [],
            rankingRBs: [],
            rankingTEs: [],
            showRankings: 'QB',
            openPop: false,
            votedQB: false,
            votedWR: false,
            votedRB: false,
            votedTE: false,
            loading: true,
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
        this.handleOpen = this.handleOpen.bind(this)
        this.handleClose = this.handleClose.bind(this)
        this.handleQBButton = this.handleQBButton.bind(this)
        this.handleWRButton = this.handleWRButton.bind(this)
        this.handleRBButton = this.handleRBButton.bind(this)
        this.handleTEButton = this.handleTEButton.bind(this)
        this.handleVotedRB = this.handleVotedRB.bind(this)
        this.handleVotedWR = this.handleVotedWR.bind(this)
        this.handlevotedQB = this.handlevotedQB.bind(this)
        this.handleVotedTE = this.handleVotedTE.bind(this)
    }

    async componentDidMount(){
        fetch('/api/get-weekly-voting'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {
            console.log(data)
            this.setState({
                loading:false,
                votingQBs: data.slice(0,3),
                votingWRS: data.slice(3,6),
                votingRBs: data.slice(6,9),
                votingTEs: data.slice(9,12)
                // mean_values: data.mean_values,
                // mode_values: data.mode_values,
                // median_values: data.median_values,
                // num_bids: data.num_bids,
                // visibleTargets: data.visibleTargets
            });

        });
        fetch('/api/get-weekly-rankings'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {
            this.setState({

                rankingQBs: data.slice(0,25),
                rankingWRs: data.slice(25,75),
                rankingRBs: data.slice(125,175),
                rankingTEs: data.slice(175,200),
            });
            document.getElementById("qbButton").style.backgroundColor = "#DD6E42";
        });
    }

    handleQBButton(e){
        document.getElementById("qbButton").style.backgroundColor = "#DD6E42";
        document.getElementById("wrButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("rbButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("teButton").style.backgroundColor = "#4F6D7A";
        this.setState({showRankings:'QB'})


        //this.reloadPage;
    }

    handleWRButton(e){
        document.getElementById("wrButton").style.backgroundColor = "#DD6E42";
        document.getElementById("qbButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("rbButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("teButton").style.backgroundColor = "#4F6D7A";
        this.setState({showRankings:'WR'})


        //this.reloadPage;
    }


    handleRBButton(e){
        document.getElementById("rbButton").style.backgroundColor = "#DD6E42";
        document.getElementById("wrButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("qbButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("teButton").style.backgroundColor = "#4F6D7A";
        this.setState({showRankings:'RB'})



        //this.reloadPage;
    }

    handleTEButton(e){
        document.getElementById("teButton").style.backgroundColor = "#DD6E42";
        document.getElementById("wrButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("rbButton").style.backgroundColor = "#4F6D7A";
        document.getElementById("qbButton").style.backgroundColor = "#4F6D7A";
        this.setState({showRankings:'TE'})


        //this.reloadPage;
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

    handlevotedQB = (index) => {

        let newRank = this.state.votingQBs[index].avg_rank -(index)
        let playerid = this.state.votingQBs[index].id
        
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
            votedQB: true,
        })
    }

    handleVotedWR = (index) => {
        console.log(index)

        
        let newRank = this.state.votingWRS[index].avg_rank -(index)
        let playerid = this.state.votingWRS[index].id
        
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
            votedWR: true,
        })
    }

    handleVotedRB = (index) => {
        console.log(index)

        
        let newRank = this.state.votingRBs[index].avg_rank -(index )
        let playerid = this.state.votingRBs[index].id
        
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
            votedRB: true,
        })
    }

    handleVotedTE = (index) => {
        console.log(index)

        
        let newRank = this.state.votingTEs[index].avg_rank -(index )
        let playerid = this.state.votingTEs[index].id
        
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
            votedTE: true,
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
                    this.state.votedQB ? (
                        this.state.votedWR ? (
                            this.state.votedRB ? (
                                this.state.votedTE ? (
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
                                        You just voted for three rankings adjustments for the half PPR weekly rankings
                                        </Typography>
                                        </li>
                                        <li>
                                        <Typography component='h5' variant='h5'>
                                        On the left column you see the consensus based off user rankings
                                        </Typography>
                                        </li>
                                        <li>
                                        <Typography component='h5' variant='h5'>
                                        On the right you can see the comparison to ECR (Expert Consensus Rankings) to show the sentiment of fantasy nerds versus the actual public
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
                                            Week {this.weekNumber} Rankings</div>
                                            </Typography>

                                            <Typography align="center" component='h5' variant='h5' >
                                            <div>Crowd Sourced Rankings</div><br></br>
                                            <Button 
                                                variant="contained" 
                                                color="primary" 
                                                onClick={this.handleOpen}>
                                                How it works
                                                </Button>
                                                </Typography>
                                                <Typography align="center" component='h5' variant='h5' >
                                            <a href=" http://faablabapp.draftdash.hop.clickbank.net"><img border="0" src="http://www.draftdashboard.com/creatives/draftdashboard300x250.gif" width="300" height="250"/></a>
                                            </Typography>
                                            <Typography align="center" component='h5' variant='h5' >
                                            <div>Click to view by position</div><br></br>
                                            </Typography>
                                                <Button 
                                                variant="contained" 
                                                color="primary" 
                                                id="qbButton"
                                                onClick={this.handleQBButton}>
                                                QB
                                                </Button>

                                                <Button 
                                                variant="contained" 
                                                color="primary" 
                                                id="rbButton"
                                                onClick={this.handleRBButton}>
                                                RB
                                                </Button>
                                                <Button 
                                                variant="contained" 
                                                color="primary" 
                                                id="wrButton"
                                                onClick={this.handleWRButton}>
                                                WR
                                                </Button>
                                                <Button 
                                                variant="contained" 
                                                color="primary" 
                                                id="teButton"
                                                onClick={this.handleTEButton}>
                                                TE
                                                </Button>
                                            <TableContainer component={Paper}>
                                            <Table  aria-label="simple table">
                                            <TableHead>
                                                <TableRow>
                                                <TableCell>FAABLab Rk.</TableCell>
                                                <TableCell>Player</TableCell>
                                                {/* <TableCell>Team</TableCell>
                                                <TableCell>Position</TableCell>  */}
                                                <TableCell>Expert Rk. (Δ)</TableCell>   
                                                {/* <TableCell>Positional Rank</TableCell> */}
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {/* <TableRow>
                                                    <TableCell>dsafdsa</TableCell>
                                                    <TableCell>ddsdfasd</TableCell>
                                                    <TableCell>asdfd</TableCell>
                                                </TableRow> */}
                                                
                                                {
                                                this.state.showRankings == 'QB' &&
                                                this.state.rankingQBs.map((row,index) => (
                                                
                                                    <TableRow key={index+1}>
                                                        <TableCell>{index+1}</TableCell>
                                                        <TableCell>{row.name} <br></br> ({row.position_type} | {row.abbreviation})</TableCell>
                                                        {/* <REPLACE 5 WITH THE ADP THAT YOU ADD TO MODELS*/}
                                                        {(index+1)>row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "red"}}>({(row.ecr-1-index)})</span></TableCell>}
                                                        {(index+1)<row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "green"}}>(+{(row.ecr-index-1)})</span></TableCell>}
                                                        {(index+1)==row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "gray"}}>(-)</span></TableCell>}
                                                    </TableRow>)
                                                ) }
                                                                                                {
                                                this.state.showRankings == 'WR' &&
                                                this.state.rankingWRs.map((row,index) => (
                                                
                                                    <TableRow key={index+1}>
                                                        <TableCell>{index+1}</TableCell>
                                                        <TableCell>{row.name} <br></br> ({row.position_type} | {row.abbreviation})</TableCell>
                                                        {/* <REPLACE 5 WITH THE ADP THAT YOU ADD TO MODELS*/}
                                                        {(index+1)>row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "red"}}>({(row.ecr-1-index)})</span></TableCell>}
                                                        {(index+1)<row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "green"}}>(+{(row.ecr-index-1)})</span></TableCell>}
                                                        {(index+1)==row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "gray"}}>(-)</span></TableCell>}
                                                    </TableRow>)
                                                ) }
                                                                                                {
                                                this.state.showRankings == 'RB' &&
                                                this.state.rankingRBs.map((row,index) => (
                                                
                                                    <TableRow key={index+1}>
                                                        <TableCell>{index+1}</TableCell>
                                                        <TableCell>{row.name} <br></br> ({row.position_type} | {row.abbreviation})</TableCell>
                                                        {/* <REPLACE 5 WITH THE ADP THAT YOU ADD TO MODELS*/}
                                                        {(index+1)>row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "red"}}>({(row.ecr-1-index)})</span></TableCell>}
                                                        {(index+1)<row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "green"}}>(+{(row.ecr-index-1)})</span></TableCell>}
                                                        {(index+1)==row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "gray"}}>(-)</span></TableCell>}
                                                    </TableRow>)
                                                ) }
                                                                                                {
                                                this.state.showRankings == 'TE' &&
                                                this.state.rankingTEs.map((row,index) => (
                                                
                                                    <TableRow key={index+1}>
                                                        <TableCell>{index+1}</TableCell>
                                                        <TableCell>{row.name} <br></br> ({row.position_type} | {row.abbreviation})</TableCell>
                                                        {/* <REPLACE 5 WITH THE ADP THAT YOU ADD TO MODELS*/}
                                                        {(index+1)>row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "red"}}>({(row.ecr-1-index)})</span></TableCell>}
                                                        {(index+1)<row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "green"}}>(+{(row.ecr-index-1)})</span></TableCell>}
                                                        {(index+1)==row.ecr && 
                                                        <TableCell>{row.ecr}  <span style={{color: "gray"}}>(-)</span></TableCell>}
                                                    </TableRow>)
                                                ) }
                                                
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
                            )  )
                            :( <Container maxWidth="md">
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
                                            
                                            ><div >Select which TE you'd start (half PPR)</div>
                                            </Typography>
                                
                                <Typography align="center">
                                {this.state.votingTEs.map((row,index) => (
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={() => this.handleVotedTE(index)}>
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
                                            (4/4)</div>
                                            </Typography>
                                    
                                    </Typography>
                            </Box>
                        </Container>)):( <Container maxWidth="md">
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
                                            
                                            ><div >Select which RB you'd start (half PPR)</div>
                                            </Typography>
                                
                                <Typography align="center">
                                {this.state.votingRBs.map((row,index) => (
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={() => this.handleVotedRB(index)}>
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
                                            (3/4)</div>
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
                                            ><div >Select which WR you start (half PPR)</div>
                                            </Typography>

                                
                                <Typography align="center">
                                {this.state.votingWRS.map((row,index) => (
                                        <Button 
                                        variant="contained" 
                                        color="primary" 
                                        onClick={() => this.handleVotedWR(index)}>
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
                                            (2/4)</div>
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
                                            ><div >Select which QB you'd start</div>
                                            </Typography>
                        
                                <Typography align="center">
                                {this.state.loading ? (<CircularProgress /> ):(
                                this.state.votingQBs.map((row,index) => (
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={() => this.handlevotedQB(index)}>
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
                                            (1/4)</div>
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