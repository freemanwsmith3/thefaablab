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
      this.state = {data: null}

  }

  async componentDidMount(){
    fetch("/api/get-data" + "?week=" + this.weekNumber + "?target=" + this.target)
    .then((response) => response.json())
    .then((data) => {

      this.setState({
          hist_data: [
            {
              name: "<10%",
              pv: data.first_bin
            },
            {
              name: "20-30%",
              pv: data.second_bin
            },
            {
              name: "30-40%",
              pv: data.third_bin
            },
            {
              name: "40-50%",
              pv: data.fourth_bin
            },
            {
              name: ">50%",
              pv: data.fifth_bin
            }]
        });
      });
    }
      
  

  render(){
    return (
      <BarChart
        width={250}
        height={350}
        data={this.state.hist_data}
        margin={{
          top: 50,
          right: 25,
          left: 0,
          bottom: 0
        }}
        barSize={15}
      >
        <XAxis dataKey="name" >
          {/* <Label value="% of FAAB Budget"  position="Bottom" /> */}
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

