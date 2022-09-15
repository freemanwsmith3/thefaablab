import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
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
          name: 0,
          pv: 4000,
          uv: 2400,
          amt: 2400
        },
        {
          name: 1,
          pv: 3000,
          uv: 1398,
          amt: 2210
        },
        {
          name: 2,
          pv: 2000,
          us: 9800,
          amt: 2290
        }]
  }

  async componentDidMount(){
    fetch("/api/get-data" + "?week=" + this.weekNumber + "?target=" + this.target)
    .then((response) => response.json())
    .then((data) => console.log(data))
    };
  

  render(){
  return(

    <BarChart
    layout="vertical"  
    width={250}
      height={4000}
      data={this.data}
      barSize={20}
    >
      <YAxis dataKey="name" />
      <XAxis />
      <Tooltip />
      <Legend />
      <CartesianGrid strokeDasharray="3 3" />
      <Bar dataKey="pv" fill="#8884d8" background={{ fill: "#eee" }} />
    </BarChart>
  );
  };
}

