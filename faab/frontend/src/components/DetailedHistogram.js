import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Label,
  LabelList
} from "recharts";
import React, { Component} from "react";




//window.location.reload(); 
//console.log(this.state)




export default class DetailedHistogram extends Component {


  constructor(props) {
      super(props);
      this.target = this.props.target;
      this.weekNumber = this.props.weekNumber;
      this.data = [
        {
          name: "0-5",
          pv: 5
        },
        {
          name: "5-10",
          pv: 10
        },
        {
          name: "10-15",
          pv: 20
        },
        {
          name: "15-20",
          pv: 15
        }]
  }

  async componentDidMount(){
    fetch("/api/get-data" + "?week=" + this.weekNumber + "?target=" + this.target)
    .then((response) => response.json())
    .then((data) => console.log(data))
    };
  

  render(){
    return (
      <BarChart
        width={250}
        height={350}
        data={this.data}
        margin={{
          top: 50,
          right: 5,
          left: 5,
          bottom: 0
        }}
        barSize={15}
      >
        <XAxis >
          <Label value="% of FAAB Budget"  position="Bottom" />
        </XAxis>
        <YAxis width={0} ticks={false}>
         <Label value="Bids"  position="left" />
        </YAxis>
        <CartesianGrid strokeDasharray="3 3" />
        <Bar dataKey="pv" fill="#8884d8"   barCategoryGap={10}>
        <LabelList dataKey="pv" position="top" />
        </Bar> 
      </BarChart>
    );
  };
}

