import React, { useEffect, useState } from "react";
import {
  Button,
  TextField,
  Grid,
  Select,
  InputLabel,
  MenuItem,
  FormControl,
  makeStyles,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Checkbox,
} from "@material-ui/core";
import DataPlot from "./DataPlot";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 130,
  },
}));

const axios = require("axios");

const baseURL = "http://127.0.0.1:8000/";

const QueryInputs = (props) => {
  const [gender, setGender] = useState("");
  const [citizenship, setCitizenship] = useState("");
  const [universityType, setUniversityType] = useState("");
  const [uniDegreeType, setUniDegreeType] = useState("");
  const [geoRegionMax, setGeoRegionMax] = useState("");
  const [region, setRegion] = useState({
    NewEngland: false,
    MidEast: false,
    GreatLakes: false,
    Plains: false,
    Southeast: false,
    Southwest: false,
    RockyMountains: false,
    FarWest: false,
    Other: false,
  });
  const {
    NewEngland,
    MidEast,
    GreatLakes,
    Plains,
    Southeast,
    Southwest,
    RockyMountains,
    FarWest,
    Other,
  } = region;

  const [startDate, setStartDate] = useState(0);
  const [endDate, setEndDate] = useState(0);
  const [urm, setURM] = useState({
    AIAN: false,
    BAA: false,
    HL: false,
    NHPI: false,
  });
  const { AIAN, BAA, HL, NHPI } = urm;
  const [states, setStates] = useState("");
  const [degree, setDegree] = useState("");
  const [method, setMethod] = useState("");
  const [data, setData] = useState(null);
  const [minDegrees, setMinDegrees] = useState("");

  const classes = useStyles();

  useEffect(() => {
    setData(null);
  }, [props.queryType]);

  const itemSpacing = 2;

  let startDateTest =
    startDate != null &&
    /[0-9]{4}/.test(startDate) &&
    startDate >= 1997 &&
    startDate <= 2019 &&
    startDate <= endDate;

  let endDateTest =
    endDate != null &&
    /[0-9]{4}/.test(endDate) &&
    endDate >= 1997 &&
    endDate <= 2019;

  let statesTest = states != null && /[A-Z]{2}/.test(states);

  let minDegreesTest = /[0-9]+/.test(minDegrees);

  const handleURM = (event) => {
    setURM({ ...urm, [event.target.name]: event.target.checked });
  };

  const handleRegion = (event) => {
    setRegion({ ...region, [event.target.name]: event.target.checked });
  };

  const top_10_urm = () => {
    axios({
      method: "get",
      url:
        baseURL +
        "query/top_10_urm" +
        "?year=" +
        endDate +
        "&degree=" +
        degree +
        "&method=" +
        method,
    }).then(function (response) {
      setData(JSON.parse(response.data));
      console.log(response.data);
    });
  };

  const urm_students_large_inst = () => {
    axios({
      method: "get",
      url:
        baseURL +
        "query/urm_students_large_inst" +
        "?year=" +
        endDate +
        "&method=" +
        method +
        "&min_awards=" +
        minDegrees,
    }).then(function (response) {
      setData(JSON.parse(response.data));
      console.log(response.data);
    });
  };

  if (props.queryType === "top_10_urm") {
    return (
      <div>
        <Grid container spacing={3} alignItems="center" alignContent="center">
          <Grid item xs={itemSpacing}>
            <TextField
              label="Year"
              required={true}
              helperText={endDateTest ? "" : "Invalid"}
              onChange={(event) => setEndDate(event.target.value)}
              inputProps={{ maxLength: 4 }}
            />
          </Grid>
          <Grid item xs={itemSpacing}>
            <FormControl className={classes.formControl}>
              <InputLabel>Degree</InputLabel>
              <Select
                value={degree}
                onChange={(event) => setDegree(event.target.value)}
              >
                <MenuItem value="PhD">PhD</MenuItem>
                <MenuItem value="MS">MS</MenuItem>
                <MenuItem value="BS">BS</MenuItem>
                <MenuItem value="A">A</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={itemSpacing}>
            <FormControl className={classes.formControl}>
              <InputLabel>Method</InputLabel>
              <Select
                value={method}
                onChange={(event) => setMethod(event.target.value)}
              >
                <MenuItem value="absolute">Absolute</MenuItem>
                <MenuItem value="percentage">Percentage</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={itemSpacing}>
            <Button
              disabled={!(endDateTest && degree && method)}
              color="primary"
              variant="contained"
              onClick={top_10_urm}
            >
              Search!
            </Button>
          </Grid>
        </Grid>
        {data != null && data.INSTNM != undefined ? (
          <DataPlot data={data} title={"Top 10 URM Univeristies"}></DataPlot>
        ) : (
          <div></div>
        )}
      </div>
    );
  } else if (props.queryType === "urm_students_large_inst") {
    return (
      <div>
        <Grid container spacing={3} alignItems="center" alignContent="center">
          <Grid item xs={itemSpacing}>
            <TextField
              label="Year"
              required={true}
              helperText={endDateTest ? "" : "Invalid"}
              onChange={(event) => setEndDate(event.target.value)}
              inputProps={{ maxLength: 4 }}
            />
          </Grid>
          <Grid item xs={itemSpacing}>
            <FormControl className={classes.formControl}>
              <InputLabel>Method</InputLabel>
              <Select
                value={method}
                onChange={(event) => setMethod(event.target.value)}
              >
                <MenuItem value="absolute">Absolute</MenuItem>
                <MenuItem value="percentage">Percentage</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={itemSpacing}>
            <TextField
              label="Minimum Degrees"
              required={true}
              helperText={minDegreesTest ? "" : "Invalid"}
              onChange={(event) => setMinDegrees(event.target.value)}
            />
          </Grid>
          <Grid item xs={itemSpacing}>
            <Button
              disabled={!(endDateTest && method && minDegreesTest)}
              color="primary"
              variant="contained"
              onClick={urm_students_large_inst}
            >
              Search!
            </Button>
          </Grid>
        </Grid>
        {data != null && data.INSTNM != undefined ? (
          <DataPlot
            data={data}
            title={"Top 10 URM with at least " + minDegrees + "awards"}
          ></DataPlot>
        ) : (
          <div></div>
        )}
      </div>
    );
  }
  return (
    <div>
      <Grid container spacing={3} alignItems="center" alignContent="center">
        <Grid item xs={itemSpacing}>
          <TextField
            label="Start Date"
            required={true}
            helperText={startDateTest ? "" : "Invalid"}
            onChange={(event) => setStartDate(event.target.value)}
            inputProps={{ maxLength: 4 }}
          />
        </Grid>
        <Grid item xs={itemSpacing}>
          <TextField
            label="End Date"
            required={true}
            helperText={endDateTest ? "" : "Invalid"}
            onChange={(event) => setEndDate(event.target.value)}
            inputProps={{ maxLength: 4 }}
          />
        </Grid>
        <Grid item xs={itemSpacing}>
          <TextField
            label="States"
            required={true}
            helperText={statesTest ? "" : "Invalid"}
            onChange={(event) => setStates(event.target.value)}
          />
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl className={classes.formControl}>
            <InputLabel>Gender</InputLabel>
            <Select
              value={gender}
              onChange={(event) => setGender(event.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="male">Male</MenuItem>
              <MenuItem value="female">Female</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl className={classes.formControl}>
            <InputLabel>Citizenship</InputLabel>
            <Select
              value={citizenship}
              onChange={(event) => setCitizenship(event.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="non-US">non-US</MenuItem>
              <MenuItem value="US">US</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl className={classes.formControl}>
            <InputLabel>University Type</InputLabel>
            <Select
              value={universityType}
              onChange={(event) => setUniversityType(event.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="public">Public</MenuItem>
              <MenuItem value="private">Private</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl className={classes.formControl}>
            <InputLabel>Degree Level</InputLabel>
            <Select
              value={uniDegreeType}
              onChange={(event) => setUniDegreeType(event.target.value)}
            >
              <MenuItem value="PhD">PhD</MenuItem>
              <MenuItem value="MS">MS</MenuItem>
              <MenuItem value="BS">BS</MenuItem>
              <MenuItem value="A">A</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl className={classes.formControl}>
            <InputLabel>Geo Location</InputLabel>
            <Select
              value={geoRegionMax}
              onChange={(event) => setGeoRegionMax(event.target.value)}
            >
              <MenuItem value="all">All</MenuItem>
              <MenuItem value="states">States</MenuItem>
              <MenuItem value="contiguous_48">Continental 48</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl required>
            <FormLabel>Region</FormLabel>
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={NewEngland}
                    value={NewEngland}
                    onChange={handleRegion}
                    name="NewEngland"
                  />
                }
                label="New England (CT, ME, MA, NH, RI, VT)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={MidEast}
                    value={MidEast}
                    onChange={handleRegion}
                  />
                }
                label="Mid East (DE, DC, MD, NJ, NY, PA)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={GreatLakes}
                    value={GreatLakes}
                    onChange={handleRegion}
                    name="GreatLakes"
                  />
                }
                label="Great Lakes  (IL, IN, MI, OH, WI)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={Plains}
                    value={Plains}
                    onChange={handleRegion}
                    name="Plains"
                  />
                }
                label="Plains (IA, KS, MN, MO, NE, ND, SD)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={Southeast}
                    value={Southeast}
                    onChange={handleRegion}
                    name="Southeast"
                  />
                }
                label="Southeast (AL, AR, FL, GA, KY, LA, MS, NC, SC, TN, VA, WV)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={Southwest}
                    value={Southwest}
                    onChange={handleRegion}
                    name="Southwest"
                  />
                }
                label="Southwest (AZ, NM, OK, TX)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={RockyMountains}
                    value={RockyMountains}
                    onChange={handleRegion}
                    name="RockyMountains"
                  />
                }
                label="Rocky Mountains (CO, ID, MT, UT, WY)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={FarWest}
                    value={FarWest}
                    onChange={handleRegion}
                    name="FarWest"
                  />
                }
                label="Far West (AK, CA, HI, NV, OR, WA)"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={Other}
                    value={Other}
                    onChange={handleRegion}
                    name="Other"
                  />
                }
                label="Other U.S. jurisdictions (AS, FM, GU, MH, MP, PR, PW, VI)"
              />
            </FormGroup>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <FormControl required>
            <FormLabel>Under Represented Minority Group</FormLabel>
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={AIAN}
                    value={AIAN}
                    name="AIAN"
                    onChange={handleURM}
                  />
                }
                label="American Indian or Alaska Native"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={BAA}
                    value={BAA}
                    name="BAA"
                    onChange={handleURM}
                  />
                }
                label="Black or African American"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={HL}
                    value={HL}
                    onChange={handleURM}
                    name="HL"
                  />
                }
                label="Hispanic or Latino"
              />
              <FormControlLabel
                control={
                  <Checkbox
                    checked={NHPI}
                    value={NHPI}
                    onChange={handleURM}
                    name="NHPI"
                  />
                }
                label="Native Hawaiian or Other Pacific Islander"
              />
            </FormGroup>
          </FormControl>
        </Grid>
        <Grid item xs={itemSpacing}>
          <Button
            disabled={
              !(
                startDateTest &&
                endDateTest &&
                gender &&
                citizenship &&
                universityType &&
                uniDegreeType &&
                geoRegionMax &&
                (NewEngland ||
                  MidEast ||
                  GreatLakes ||
                  Plains ||
                  Southeast ||
                  Southwest ||
                  RockyMountains ||
                  FarWest ||
                  Other) &&
                (AIAN || BAA || HL || NHPI)
              )
            }
            color="primary"
            variant="contained"
            onClick={top_10_urm}
          >
            Search!
          </Button>
        </Grid>
        {data != null ? (
          <DataPlot
            data={{
              INSTNM: [
                "Miami Dade College",
                "Broward College",
                "Valencia College",
                "Santa Ana College",
                "University of Phoenix-Arizona",
                "Central Georgia Technical College",
                "Atlanta Technical College",
                "East Los Angeles College",
                "Chattahoochee Technical College",
                "Rio Salado College",
              ],
              CSTOTLT: [
                4470, 3626, 4383, 2873, 5701, 3597, 1617, 2085, 3613, 2554,
              ],
              URM: [3663, 2392, 2159, 1988, 1939, 1727, 1501, 1317, 1313, 1201],
            }}
          ></DataPlot>
        ) : (
          <div></div>
        )}
      </Grid>
    </div>
  );
};

export default QueryInputs;
