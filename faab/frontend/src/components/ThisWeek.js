import React, { Component} from "react";
import ShowData from "./ShowData";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import BidPlayer from "./BidPlayer";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Container from '@material-ui/core/Container';
import Box from '@material-ui/core/Box';
import Stack from '@material-ui/core/Stack';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core//Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';

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
                <Grid container spacing={1} >
                    <div id="app">
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
                                <Typography variant="h5" align="center" color="text.secondary" paragraph>
                                Submit a Mock Bid to View Average Responses
                                </Typography>

                            </Container>
                        </Box>                        
                        <Container sx={{ py: 8 }} maxWidth="md">
                        {/* End hero unit */}
                        <Grid container spacing={4}>
                            {this.state.visibleTargets.map((visible, index) => {    
                                return visible ? ( 
                                    <Grid  item key={index}xs={12} sm={6} md={4}>
                                        <Card
                                        sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                                        >
                                        <CardMedia
                                            component="img"
                                            sx={{
                                            // 16:9
                                            pt: '56.25%',
                                            }}
                                            alt="random"
                                        />

                                        <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography gutterBottom variant="h5" component="h2">
                                        Heading
                                        </Typography>
                                        <Typography>
                                        This is a media card. You can use this section to describe the
                                        content.
                                        </Typography>
                                        </CardContent>
                                        <CardActions>
                                            <Button size="small">View</Button>
                                            <Button size="small">Edit</Button>
                                        </CardActions>
                                        </Card>
                                    </Grid>) :(
                                        <BidPlayer weekNumber={this.weekNumber}  target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]}  link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]}  />
                                    
                            )})}
                            </Grid>
                        </Container>         
                    </div>
                </Grid> 
        )
    }
}
                            {/* return visible ? (
                                <div>
                                    <ShowData weekNumber={this.weekNumber} target={this.state.targets[index]} name = {this.state.names[index]} team = {this.state.teams[index]} link = {this.state.links[index]}  image = {this.state.images[index]} position = {this.state.positions[index]} mean_value = {this.state.mean_values[index]} mode_value = {this.state.mode_values[index]} median_value = {this.state.median_values[index]} num_bid = {this.state.num_bids[index]} />
                                </div> )  : (

                                )   
                            })} */}