import { AppBar, Toolbar, IconButton, Typography} from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';

const Appbar = () =>{
    return (
        <div >
          <AppBar position="static">
            <Toolbar variant="dense">
              <IconButton edge="start" color="inherit" aria-label="menu">
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" color="inherit">
                MAUI
              </Typography>
            </Toolbar>
          </AppBar>
        </div>
      );
}

export default Appbar