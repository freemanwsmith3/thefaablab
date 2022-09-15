import React, { Component } from "react";
import Box from "@material-ui/core/Box";
import Container from "@material-ui/core/Container";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import Card from '@material-ui/core//Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import DetailedHistogram from "./DetailedHistogram";

export default class ShowData extends Component {
    constructor(props) {
        super(props);
        this.state = {
            mean_value: 0,
            openPop: false
            //visibleTargets: null,
            // visibleTargets: 1,
        };
        this.target = this.props.target;
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


    // }


    render() {
        return (
       
            <Grid  xs={12} sm={6} md={4 } >
                <Card
                sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                >
                <CardContent sx={{ flexGrow: 1, border: 1 } }>
                <div align='center'>
                    <Typography component='h5' variant='h5'>
                        {this.name} - {this.position}
                    </Typography>
                    <Typography component='h6' variant='h6'>
                        {this.team}
                    </Typography>
                </div>
                
                <Box sx={{ p: 2, border: '1px dashed grey' }}>
                    <Typography component='h5' variant='h5'>
                    Average Bid:  {this.mean_value.toString()}%
                    </Typography>
                    <Typography component='h5' variant='h5'>
                        Median Bid:  {this.median_value.toString()}%
                    </Typography>
                    <Typography component='h5' variant='h5'>
                        Number of Bids:  {this.num_bid.toString()}
                    </Typography>
                    <Typography align = "center" component='h5' variant='h5'>
                    </Typography>
                </Box>
                <Container maxWidth="md">

                        <DetailedHistogram sx={{ height: '100%',  width: '100%'}} weekNumber={this.weekNumber} target={this.target} />

                </Container>
            </CardContent>
                    {/* <CardActions>

                    </CardActions> */}
                </Card>
            </Grid> 
        );
      }
    }