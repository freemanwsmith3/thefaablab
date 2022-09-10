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
import Fade from '@material-ui/core/Fade';
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { createTheme, ThemeProvider } from '@material-ui/core/styles';


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
            visibleTargets: []
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
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

    

    render(){
        return(
            <html>
                <ThemeProvider theme={this.theme}>
                <CssBaseline />
                <header>
                    <AppBar position="relative">
                        <Toolbar>
                            
                        {/* <SportsFootballOutlinedIcon sx={{ mr: 2 }} /> */}
                        <Typography variant="h3" color="inherit" noWrap>
                            FaabLab
                        </Typography>
                        </Toolbar>
                    </AppBar>
                </header>
                <main id="app">
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
                            <Typography variant="h6" align="left" color="text.secondary"  >
                            <ul>
                                <li>Submit how much FAAB you will bid on a player </li>
                                <li>Bid in % of your start of season FAAB</li>
                                <li>After submission, consensus bid data will be revealed </li>
                            </ul>
                            </Typography>


                        </Container>
                    </Box>                        
                    <Container sx={{ py: 8 }} maxWidth="md">
                    {/* End hero unit */}
                        <Grid container spacing={4}>
                            {this.state.visibleTargets.map((visible, index) => {    
                                return visible ? ( 
                                    <ShowData index = {index} weekNumber={this.weekNumber} target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]} link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]} mean_value = {this.state.mean_values[index]} mode_value = {this.state.mode_values[index]} median_value = {this.state.median_values[index]} num_bid = {this.state.num_bids[index]} />

                                    ) :(
                                    <BidPlayer index = {index} weekNumber={this.weekNumber}  target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]}  link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]}  />
                                )
                            })}
                        </Grid>
                    </Container>         
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