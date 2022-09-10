import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import Card from '@material-ui/core//Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';


export default class ShowData extends Component {
    constructor(props) {
        super(props);
        this.state = {
            mean_value: 0,
            //visibleTargets: null,
            // visibleTargets: 1,
        };
        this.weekNumber = this.props.weekNumber;
        this.name = this.props.name;
        this.team = this.props.team;
        this.link = this.props.link;
        this.image = this.props.image;
        this.position = this.props.position;
        this.mean_value = this.props.mean_value;
        this.mode_value = this.props.mode_value;
        this.median_value = this.props.median_value;
        this.num_bid = this.props.num_bid;
    }

    // async componentDidMount(){
    //     fetch('/api/user-did-bid')
    //     .then((response)=> response.json())
    //     .then((data) => {
    //         this.setState({
    //         visibleTargets: data.visibleTargets
    //         });
    //     });
    //     console.log(this.state)
    // }


    // getWeekDetails(){
    //     fetch("/api/get-week" + "?week=" + this.weekNumber)
    //     .then((response) => response.json())
    //     .then((data) => {
    //       this.setState({
    //         player: data[0].player,
    //         //guestCanPause: data.guestsCanSee,
    //         mean_value: data[0].mean_value,
    //       });
    //     });
        
    // }

    render() {
        return (
       
            <Grid  xs={12} sm={6} md={4 } >
                <Card
                sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                >
                    <CardMedia
                        component="img"
                        sx={{
                        // 16:9
                        pt: '56.25%',
                        }}
                        image={this.image}
                        alt="random"
                    />
    
                      <CardContent sx={{ flexGrow: 1, border: 1 } }>
                        <Typography component='h5' variant='h5'>
                            {this.name}
                        </Typography>
                        <Typography component='h6' variant='h6'>
                            {this.team}
                        </Typography>
                        <Typography component='h7' variant='h7'>
                            {this.position}
                        </Typography>
                        <Typography component='h5' variant='h5'>
                        Average Bid:  {this.mean_value.toString()}%
                      </Typography>
                      <Typography component='h5' variant='h5'>
                        Median Bid:  {this.median_value.toString()}%
                      </Typography>
                      <Typography component='h5' variant='h5'>
                        Most Common Bid:  {this.mode_value.toString()}%
                      </Typography>
                      <Typography component='h5' variant='h5'>
                        Number of Bids:  {this.num_bid.toString()}
                        </Typography>
                    </CardContent>
                    <CardActions>
                    {/* <Button
                                //className={classes.button}
                                variant="contained" 
                                color="primary" 
                                type="submit" 
                                //endIcon={<Icon>SportsFootball</Icon>}
                                //defaultValue="true"
                                onClick={this.handleBidButtonPress}
                                >Submit</Button> */}
                        {/* <Button size="small">View</Button>
                        <Button size="small">Edit</Button> */}
                    </CardActions>
                </Card>
            </Grid> 
        );
      }
    }