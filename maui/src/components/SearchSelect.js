import React from "react";
import {
  Select,
  InputLabel,
  MenuItem,
  FormControl,
  makeStyles,
} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 130,
  },
}));

const SelectSearch = (props) => {

  const classes = useStyles();

  return (
    <FormControl className={classes.formControl}>
      <InputLabel>Query Type</InputLabel>
      <Select
        value={props.queryType}
        onChange={(event) => props.setQueryType(event.target.value)}
      >
        <MenuItem value="top_10_urm">Top 10 URM Universities</MenuItem>
        <MenuItem value="urm_degrees">URM Degrees Advanced Query</MenuItem>
        <MenuItem value="find_major_universities">
          Major Universities Query
        </MenuItem>
        <MenuItem value="urm_students_large_inst">
        URM Degrees with minimum Degrees Awarded
        </MenuItem>
      </Select>
    </FormControl>
  );
};

export default SelectSearch;
