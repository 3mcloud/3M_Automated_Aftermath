import {React} from "react";
import {
  Select,
  InputLabel,
  FormControl,
  makeStyles,
  withStyles
} from "@material-ui/core";

import MuiMenuItem from "@material-ui/core/MenuItem";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: "75%",
    margin:".5%"
  },
}));

const MenuItem = withStyles({
  root: {
    justifyContent: "center",
  }
})(MuiMenuItem);

const SelectSearch = (props) => {

const classes = useStyles();

  return (
    <FormControl className={classes.formControl}>
      <InputLabel>Query Type</InputLabel>
      <Select
        value={props.queryType}
        onChange={(event) => props.setQueryType(event.target.value)}
        MenuProps={{
          getContentAnchorEl: null,
          anchorOrigin: {vertical: 'bottom',horizontal: 'left' },
          transformOrigin: { vertical: 'top', horizontal: 'left' },
      }}
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
