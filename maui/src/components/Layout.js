import Query from './Query'
import React from 'react'
import { List, ListItemText,  ListItem, Divider, Grid} from '@material-ui/core';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles({
  list: {
    width: 250,
  },
  fullList: {
    width: 'auto',
  },
});


const Layout = () => {
    const classes = useStyles();

    const list = (anchor) => (
        <div
            className={clsx(classes.list, {
              [classes.fullList]: anchor === 'top' || anchor === 'bottom',
            })}
            role="presentation"
          >
          <List>
            {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
              <ListItem button key={text}>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
          <Divider />
          <List>
            {['All mail', 'Trash', 'Spam'].map((text, index) => (
              <ListItem button key={text}>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </div>
      );

    return (
      <div className="App">
            {['left'].map((anchor) => (
            <React.Fragment key={anchor}>
                {list(anchor)}
            </React.Fragment>
            ))}
      </div>
    );
  }
  
  export default Layout;