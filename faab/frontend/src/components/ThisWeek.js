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
import Card from '@material-ui/core//Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import { ClickAwayListener } from "@material-ui/core";

function themeFunction(){
    const theme = createTheme();
}

function Copyright() {
    return (
      <Typography variant="body2" color="text.secondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://faablab.app/">
          FaabLab
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }

export default class ThisWeek extends Component {
    

    constructor(props) {
        super(props);
        this.theme = themeFunction();
        this.state = {
            visibleTargets: [],
            openPop: false
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
        this.handleOpen = this.handleOpen.bind(this)
        this.handleClose = this.handleClose.bind(this)
    }

    async componentDidMount(){
        fetch('/api/get-targets'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {

            this.setState({
                names: data.names,
                teams: data.teams,
                links: data.links,
                images: data.images,
                targets: data.targets,
                positions: data.positions,
                mean_values: data.mean_values,
                mode_values: data.mode_values,
                median_values: data.median_values,
                num_bids: data.num_bids,
                visibleTargets: data.visibleTargets
            });
        });
        console.log(this.state)
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
        return(
            <html >
                <ThemeProvider theme={this.theme} >
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
                                    Below are the top waiver wire adds for the week
                                    </Typography>
                                    </li>
                                    <li>
                                    <Typography component='h5' variant='h5'>
                                    Submit what you plan to bid in your league (Bids are in % of start of season FAAB)
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
                                        >
                                        Week: {this.weekNumber}
                                        </Typography>
                                        <Typography align="center">
                                            <Button 
                                            variant="contained" 
                                            color="primary" 
                                            onClick={this.handleOpen}>
                                            How it works
                                            </Button>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br>Top Waiver Adds
                                        </Typography>
                                    </Container>
                                </Box>
                                <Box>
                                    <Container sx={{ py: 8 }} maxWidth="md">
                                                                            

                                    {/* End hero unit */}
                                        <Grid container spacing={4}>
                                        <Container align="center">

                                        </Container>
                                            {this.state.visibleTargets.map((visible, index) => {    
                                                return visible ? ( 
                                                    <ShowData weekNumber={this.weekNumber} target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]} link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]} mean_value = {this.state.mean_values[index]} mode_value = {this.state.mode_values[index]} median_value = {this.state.median_values[index]} num_bid = {this.state.num_bids[index]} />

                                                    ) :(
                                                    <BidPlayer weekNumber={this.weekNumber}  target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]}  link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]}  />
                                                )
                                            })}
                                        </Grid>
                                    </Container>        
                                </Box>      
                            </Container>
                        )  }

                   

                </main>
                <footer>
                <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
                    {/* <Typography variant="h6" align="center" gutterBottom>
                    Footer
                    </Typography>
                    <Typography
                    variant="subtitle1"
                    align="center"
                    color="text.secondary"
                    component="p"
                    >
                    Something here to give the footer a purpose!
                    </Typography> */}
                    <Copyright />
                </Box>
                </footer>
                </ThemeProvider>
            </html>
        );
        
    }
}