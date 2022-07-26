import { React } from 'react';
import { AppBar } from '@material-ui/core';
import SelectSearch from './SearchSelect'

const Appbar = (props) =>{
    return (
          <AppBar position="static"
          style={{
            display: "flex",
            alignItems: "center",
            backgroundColor: "tan",
          }}>
               <SelectSearch
               style-={{
                width: "100%",
                maxWidth: 600,
                mx: "auto"
               }}
               queryType={props.queryType} setQueryType={props.setQueryType}
                ></SelectSearch>
          </AppBar>
      );
}

export default Appbar