import React, { Component} from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import BidPlayer from "./BidPlayer";
import ThisWeek from "./ThisWeek";
import PostSeason from "./PostSeason"

export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state= {
            // This is where you set which week it is in season, use the README for more info
            week: 15,
        };
    }

    render(){
        return <Router> 
            <Switch>
                <Route exact path='/' component = {PostSeason} />
                {/* This is how to redirect to in season weeks */}
                {/* <Route exact path="/" render = {() => {
                    return(<Redirect to={`/week/${this.state.week}`}/>
                    );
                }}/> */}
                 <Route exact path='/player' component = {BidPlayer} />
                 <Route exact path='/week/:weekNumber' component = {ThisWeek} />
                 {/* <Route exact path='/week/:weekNumber/:playerName' component = {StatDetails} /> */}
            </Switch>
        </Router>
    }
}