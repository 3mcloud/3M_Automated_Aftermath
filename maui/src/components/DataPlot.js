import { React } from 'react';
import Plot from "react-plotly.js";

const DataPlot = (props) => {

  console.log(props.data.INSTNM)

  return (
    <Plot
      config={{ displayModeBar: true }}
      data={[
        {
          x: props.data.INSTNM,
          y: props.data.URM,
          name: 'URM',
          type: 'bar'
        },
        {
          x: props.data.INSTNM,
          y: props.data.CSTOTLT,
          name: 'Total',
          type: 'bar'
        },
      ]}
      layout={{ width: 600, height: 600, xaxis: {automargin: true}, title: props.title }}
    />
  );
};

export default DataPlot;