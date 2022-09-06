import React, { Component} from "react";
import ShowData from "./ShowData";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import BidPlayer from "./BidPlayer";
import Typography from "@material-ui/core/Typography";


export default class ThisWeek extends Component {
    constructor(props) {
        super(props);
        this.state = {
            visibleTargets: [],
        };
        
        this.weekNumber = this.props.match.params.weekNumber;
        this.testTarget = 2;
    }

    async componentDidMount(){
        fetch('/api/get-targets'+ "?week=" + this.weekNumber)
        .then((response)=> response.json())
        .then((data) => {

            this.setState({
                names: data.names,
                teams: data.teams,
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
            <body>

                <div id="app">
                    <Typography component='h3' variant='h3'>
                        Week: {this.weekNumber}
                    </Typography>    
                    <Typography component='h5' variant='h5'>
                        <br></br>
                        Submit a Mock Bid to View Average Responses
                        <br></br>
                        <br></br>
                    </Typography>    

                    {this.state.visibleTargets.map((visible, index) => {   
                        return visible ? (
                            <div>
                                <ShowData weekNumber={this.weekNumber} target={index} name = {this.state.names[index]} team = {this.state.teams[index]} position = {this.state.positions[index]} mean_value = {this.state.mean_values[index]} mode_value = {this.state.mode_values[index]} median_value = {this.state.median_values[index]} num_bid = {this.state.num_bids[index]} />
                            </div> )  : (
                            <div>
                                
                                <BidPlayer weekNumber={this.weekNumber}  target={index} name = {this.state.names[index]} team = {this.state.teams[index]} position = {this.state.positions[index]}  />
                            </div>
                            )   
                        })}
                </div>
            </body>
        )
    }
}