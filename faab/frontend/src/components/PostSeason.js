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
import { createTheme, ThemeProvider } from '@material-ui/core/styles';

function themeFunction(){
    const theme = createTheme();
}

function Copyright() {
    return (
      <Typography variant="body2" color="text.secondary" align="center">
        Contact: faablabapp@gmail.com
        {/* {new Date().getFullYear()}
        {'.'} */}
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
                                    Submit what you plan to bid in your league (bids are in % of start of season FAAB)
                                    </Typography>
                                    </li>
                                    <li>
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
                                        2022 Season Recap: </div>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <div>Happy offseason, enjoy the results from previous weeks</div><br></br>
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
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/2" >Week 2</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/3" >Week 3</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/4" >Week 4</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/5" >Week 5</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/6" >Week 6</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/7" >Week 7</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/8" >Week 8</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/9" >Week 9</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/10" >Week 10</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/11" >Week 11</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/12" >Week 12</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/13" >Week 13</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/14" >Week 14</a>
                                        </Typography>
                                        <Typography align="center" component='h5' variant='h5' >
                                       <br></br><a style = {{color: 'blue'}}  href="https://www.faablab.app/week/15" >Week 15</a>
                                        </Typography>

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