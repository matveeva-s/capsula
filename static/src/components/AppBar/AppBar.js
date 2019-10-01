import React, { Component } from 'react';
import { Box } from 'grommet';

const AppBar = (props) => (
    <Box
        tag='header'
        direction='row'
        align='center'
        justify='between'
        background='brand'
        pad={{ left: 'medium', right: 'small', vertical: 'xsmall' }}
        style={{ zIndex: '1' }}
        {...props}
    />
);
export default AppBar;