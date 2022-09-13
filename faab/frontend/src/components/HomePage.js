import React, { Component} from "react";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import BidPlayer from "./BidPlayer";
import ThisWeek from "./ThisWeek";



export default class HomePage extends Component {
    constructor(props) {
        super(props);
        this.state= {
            week: 2,
        };
    }

    render(){
        return <Router> 
            <Switch>
                <Route exact path="/" render = {() => {
                    return(<Redirect to={`/week/${this.state.week}`}/>
                    );
                }}/>
                 <Route exact path='/player' component = {BidPlayer} />
                 <Route exact path='/week/:weekNumber' component = {ThisWeek} />
            </Switch>
        </Router>
    }
}