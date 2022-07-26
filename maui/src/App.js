import './App.css';
import React, { useState } from "react";
import QueryInputs from './components/QueryInputs';
import Appbar from './components/Appbar';
import DataPlot from './components/DataPlot'
import SelectSearch from './components/SearchSelect';

function App() {
  const [queryType, setQueryType] = useState("");
  return (
    <div style={{

                }}>

        <Appbar setQueryType={setQueryType} queryType={queryType}></Appbar>
        <div style={{height: 10}}></div>
        <QueryInputs queryType={queryType}></QueryInputs> 
        {/* <DataPlot></DataPlot> */}
    </div>
  );
}

export default App;