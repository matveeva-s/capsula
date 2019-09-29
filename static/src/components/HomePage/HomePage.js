import React, { Component } from 'react';
import { Box } from 'grommet';

import MenuButton from './../Button/MenuButton';
import Banner from './../Banner/Banner';


export default class HomePage extends Component {

    render() {
        return (
            <Box>
                <Banner></Banner>
                <MenuButton label='button'></MenuButton>
            </Box>
        );
    }
}