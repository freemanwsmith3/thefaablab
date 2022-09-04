import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Slider from "@material-ui/core/Slider";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";

export default class BidPlayerPage extends Component {


    constructor(props) {


        
        super(props);
        this.state = {
            player: 1,
            guestsCanSee: false,
            value: null,
        };

        this.handleBidButtonPress = this.handleBidButtonPress.bind(this)
        this.handleBidValue = this.handleBidValue.bind(this)
        //this.handleGuestCanSeeChange = this.handleGuestCanSeeChange.bind(this)
    }

    handleBidValue(e){
        
        this.setState({
            value: e.target.value,

        })
        console.log(e)
    }

    handleBidButtonPress(e){

        this.setState({
            guestsCanSee: true,
        })

        const submitBid = {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                value: this.state.value,
                player: this.state.player,
                user: "786dfadsfa",
            }),

        };

        fetch("/api/bid", submitBid)
            .then((response) => response.json())
            .then((data) => console.log(data));
        //console.log(this.state)
    }


    render(){


        return <Grid container spacing={1}>
            < Grid item xs={12} align="center">
                <Typography component='h4' variant='h4'>
                    Submit a Mock Bid to View Average Responses
                </Typography>
            </Grid>
            < Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText >
                        <div align='center'>
                        <Typography component='h5' variant='h5'>
                            Jerry Jeudy
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
}