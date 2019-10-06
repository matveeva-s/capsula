import React, { Component } from 'react';
import {
    Box,
    Button,
    Collapsible,
    Heading,
    Grommet,
    Layer,
    ResponsiveContext,
} from 'grommet';
import { FormClose } from 'grommet-icons';

import { Switch, Route } from 'react-router-dom'

import Burger from '@animated-burgers/burger-slip';
import '@animated-burgers/burger-slip/dist/styles.css' 

import AppBar from './components/AppBar/AppBar';
import SearchBar from './components/SearchBar/SearchBar';
import MenuButton from './components/Button/MenuButton';
import HomePage from './components/HomePage/HomePage'
import UserAvatar from './components/UserProfile/UserAvatar';
import UserPage from './components/UserProfile/UserPage';


import { Link } from 'react-router-dom';
import styles from "./App.module.css";


const theme = {
    global: {
        colors: {
            brand: '#ffffff',
            accent: '#7d4cdb',
            contrast: '#000000',
            background: '#0000000a',
        },
        font: {
            family: 'Roboto',
            size: '14px',
            height: '20px',
        },
    },
};

class App extends Component {
    state = {
        showSidebar: false,
    }
    
    render() {
        const { showSidebar } = this.state;
        return (
            <Grommet theme={theme} full>
                <ResponsiveContext.Consumer>
                    {size => (
                        <Box>
                            <AppBar>
                                <UserAvatar></UserAvatar>
                                <Link to='/' style={{ textDecoration: 'none' }}>
                                    <Heading level='3' margin='none' alignSelf='center'>Capsula</Heading>
                                </Link>
                                
                                <Box margin={{ horizontal: "small", vertical: "xsmall" }}>
                                    <Burger
                                        onClick={() => this.setState({ showSidebar: !this.state.showSidebar })}
                                        isOpen = {this.state,showSidebar}
                                    />
                                </Box>
                            </AppBar>

                            <Box flex direction='column' overflow={{ horizontal: 'hidden' }}>
                                {(!showSidebar || size !== 'small') ? (
                                    <Collapsible direction='vertical' open={showSidebar}>
                                        <Box
                                            flex
                                            direction='row'
                                            background='brand'
                                            elevation='xsmall'
                                            align='center'
                                            justify='center'
                                            height='200px'
                                        >
                                            <SearchBar></SearchBar>
                                            <MenuButton icon='Catalog' label='My books'></MenuButton>
                                            <MenuButton label='Swaps'></MenuButton>
                                            <MenuButton label='Friends'></MenuButton>
                                        </Box>
                                    </Collapsible>
                                ): (
                                    <Layer>
                                        <Box
                                            background='brand'
                                            tag='header'
                                            justify='end'
                                            align='center'
                                            direction='row'
                                        >
                                            <Button
                                                icon={<FormClose />}
                                                onClick={() => this.setState({ showSidebar: false })}
                                            />

                                        </Box>
                                        <Box
                                            fill
                                            background='brand'
                                            align='center'
                                            justify='center'
                                        >
                                            <SearchBar></SearchBar>
                                            <MenuButton label='Swaps'></MenuButton>
                                            <MenuButton label='Proposals'></MenuButton>
                                            <MenuButton label='Active'></MenuButton>
                                            
                                        </Box>
                                    </Layer>
                                )}
                            </Box>

                            <Box flex align='center' justify='center'>
                                <Switch>
                                    <Route exact path='/' component={ HomePage }/>
                                    <Route path='/profile_id=:id' component={ UserPage }/>
                                </Switch>
                            </Box>
                        </Box>
                    )}
                </ResponsiveContext.Consumer>
            </Grommet>
        );
    }
}

export default App;