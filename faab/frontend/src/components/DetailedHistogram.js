import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
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
              name: data.first_name,
              pv: data.first_bin
            },
            {
              name: data.second_name,
              pv: data.second_bin
            },
            {
              name: data.third_name,
              pv: data.third_bin
            },
            {
              name: data.fourth_name,
              pv: data.fourth_bin
            },
            {
              name: data.fifth_name,
              pv: data.fifth_bin
            },
            {
              name: data.sixth_name,
              pv: data.sixth_bin
            },
          ]
        });
      });
    }
      
  

  render(){
    return (
      <div style={{ width: "100%", height: 350}}>
      <ResponsiveContainer>
        <BarChart
          height={350}
          layout="horizontal"
          data={this.state.hist_data}
          margin={{
            top: 60,
            right: 0,
            left: 0,
            bottom: 40
          }}
          
        >
          <XAxis ticks={false} dy={19} dataKey="name" angle={90} >
            <Label fill="#616161" dy={50} value="% of FAAB Budget"  position="Bottom" />
            <Label dy={-264}  value="# of Bids per Bid Value"  position="Top" />
          </XAxis>
          <YAxis width={0} ticks={false}>
          {/* <Label value="Bids"  position="left" /> */}
          </YAxis  >
          <Bar  barSize={20} dataKey="pv" fill="#8884d8"   >
          <LabelList dataKey="pv" position="top" />
          </Bar> 
        </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };
}

