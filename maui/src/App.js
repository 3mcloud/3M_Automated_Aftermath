import './App.css';
import React, { useState } from "react";
import QueryInputs from './components/QueryInputs';
import Appbar from './components/Appbar';
import DataPlot from './components/DataPlot'
import SelectSearch from './components/SearchSelect';

function App() {
  const [queryType, setQueryType] = useState("");
  return (
    <div className="App">

        <Appbar></Appbar>
        <SelectSearch queryType={queryType} setQueryType={setQueryType}></SelectSearch>
        <QueryInputs queryType={queryType}></QueryInputs>
        {/* <DataPlot></DataPlot> */}
    </div>
  );
}

export default App;