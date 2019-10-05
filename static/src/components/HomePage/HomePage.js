import React, { Component } from 'react';
import { Box } from 'grommet';

import MenuButton from './../Button/MenuButton';
import Banner from './../Banner/Banner';
import * as axios from "axios";


class HomePage extends Component {
 //test axios todo delete

    state = {auth_token: ""};

    async handleSubmitLogin() {
        let response  = await fetch('http://localhost:8000/auth/login/', {
            method: 'POST',
            body: JSON.stringify({
                username: "Svetik",
                password: "Capsula1337"
            })
        });

        const myJson = await response.json();
            console.log(myJson.token);
        return myJson.token;
    };

    async handleSubmitLogout(t) {
        const myJson = t.then(function(res){
        axios({
            method: 'GET',
            url: '/auth/logout/',
            headers: {'Authorization': 'Token ' + res}
        })
            .then(function (response) {
                console.log(response)
            });
    })};

    async handleSubmitMe(t){
        const myJson = t.then(function(res){
            axios({
                method: 'GET',
                url: '/user/me/',
                headers: {'Authorization': 'Token ' + res}
            })
                .then(function (response) {
                    console.log(response)
                });
        })};

    render(){
        return (
            <Box>
                <Banner/>
                    <MenuButton label='button'/>
                    <button  onClick={() => this.setState({auth_token: this.handleSubmitLogin()})}>Login</button>
                    <button  onClick={() => this.handleSubmitLogout(this.state.auth_token)}>Logout</button>
                    <button  onClick={() => this.handleSubmitMe(this.state.auth_token)}>Me</button>
            </Box>
        );
    }
}

export default HomePage;