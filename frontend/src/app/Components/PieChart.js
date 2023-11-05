import React from "react";
import Chart from "react-apexcharts";

const series = [44, 55, 41, 17, 15];
const options = {
  chart: {
    type: "donut"
  },
  plotOptions: {
    pie: {
      donut: {
        size: "50%"
      }
    }
  },
  labels:["win","draw","lose"],
  colors:["#008000","#808080","#ff0000"]
};

export default function InsightsView({data}) {
  return (
    <div>
      <Chart options={options} series={data} type="donut" height={300} />
    </div>
  );
}
