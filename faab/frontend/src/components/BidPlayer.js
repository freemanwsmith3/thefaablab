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

export default class BidPlayer extends Component {


    constructor(props) {

        super(props);
        this.state = {
            value: 0,
            week: 1,
        };
        this.index = this.props.index;
        this.weekNumber = this.props.weekNumber;
        this.target = this.props.target;
        this.name = this.props.name;
        this.team = this.props.team;
        this.link = this.props.link;
        this.image = this.props.image;
        this.position = this.props.position;
        this.mean_value = this.props.mean_value;
        this.mode_value = this.props.mode_value;
        this.median_value = this.props.median_value;
        this.num_bids = this.props.num_bids;
        this.handleBidButtonPress = this.handleBidButtonPress.bind(this)
        this.handleBidValue = this.handleBidValue.bind(this)
    }

    handleBidValue(e){

        this.setState({
            value: e.target.value,

        })
        console.log(e)
    }

    reloadPage(){
        window.location.reload(false); 
    };

    handleBidButtonPress(e){

        this.setState({
            guestsCanSee: true,
        })

        const submitBid = {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                value: this.state.value,
                target: this.target,
                week: parseInt(this.weekNumber), 
            }),

        };

        fetch("/api/bid", submitBid)
            .then((response) => response.json())
            .then((data) => console.log(data))
            .then(this.reloadPage);

        
        //window.location.reload(); 
        //console.log(this.state)

        
    }


    render(){

        
        return (
        
        <Grid item key={this.index} xs={12} sm={6} md={4}>
            <Card
            sx={{ height: '100%', display: 'flex', flexDirection: 'column'}} 
            >
                <CardMedia
                    component="img"
                    sx={{
                    // 16:9
                    pt: '56.25%',
                    }}
                    image={this.image}
                    alt={this.name}
                />

                <CardContent sx={{ flexGrow: 1, border: 1 } }>
                    <FormControl component="fieldset" style={{width:'100%'}}>
                        <FormHelperText >
                            <div align='center'>
                            <Typography component='h5' variant='h5'>
                                {this.name}
                            </Typography>
                            <Typography component='h6' variant='h6'>
                                {this.team}
                            </Typography>
                            <Typography component='h7' variant='h7'>
                                {this.position}
                            </Typography>
                            </div>
                        </FormHelperText>
                        <TextField
                            type="number"
                            name="bid"
                            label="% of initial FAAB"
                            variant="filled"
                            onFocus={(e) => e.target.value = ""}
                            InputProps={{ inputProps: { min: 0, max: 100 } }}
                            //value={inputField.bid}
                            onChange={this.handleBidValue}
                        />

                    </FormControl>


                    {/* <FormControl>
                        <Button
                            //className={classes.button}
                            variant="contained" 
                            color="primary" 
                            type="submit" 
                            //endIcon={<Icon>SportsFootball</Icon>}
                            //defaultValue="true"
                            onClick={this.handleBidButtonPress}
                            >Submit</Button>
                    </FormControl> */}
                </CardContent>
                <CardActions>
                <Button
                            //className={classes.button}
                            variant="contained" 
                            color="primary" 
                            type="submit" 
                            //endIcon={<Icon>SportsFootball</Icon>}
                            //defaultValue="true"
                            onClick={this.handleBidButtonPress}
                            >Submit</Button>
                    {/* <Button size="small">View</Button>
                    <Button size="small">Edit</Button> */}
                </CardActions>
            </Card>
        </Grid> );
        }
    }

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        {/* <Grid container spacing={1} >
            < Grid item xs={12} align="center">

            </Grid>
            < Grid item xs={12} align="center" id = 'bid-box'>
                <FormControl component="fieldset">
                    <FormHelperText >
                        <div align='center'>
                        <Typography component='h5' variant='h5'>
                            {this.name}
                        </Typography>
                        <Typography component='h6' variant='h6'>
                            {this.team}
                        </Typography>
                        <Typography component='h7' variant='h7'>
                            {this.position}
                        </Typography>
                        </div>
                    </FormHelperText>
                    <TextField
                        type="number"
                        name="bid"
                        label="Bid"
                        variant="filled"
                        defaultValue={0}
                        onFocus={(e) => e.target.value = ""}
                        InputProps={{ inputProps: { min: 0, max: 100 } }}
                        //value={inputField.bid}
                        onChange={this.handleBidValue}
                    />

                </FormControl>
            </Grid>
                <Grid item xs={12} align="center">
                    <FormControl>
                        <Button
                            //className={classes.button}
                            variant="contained" 
                            color="primary" 
                            type="submit" 
                            //endIcon={<Icon>SportsFootball</Icon>}
                            //defaultValue="true"
                            onClick={this.handleBidButtonPress}
                            >Submit</Button>
                    </FormControl>
                </Grid>
        </Grid>;

    }
} */}