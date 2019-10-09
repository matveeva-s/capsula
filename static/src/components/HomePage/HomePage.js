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
                username: "Sveta",
                password: "Capsula1337"
            })
        });

        const myJson = await response.json();
            console.log(myJson);
        return myJson.token;
    };

    async handleSubmitRegistration() {
        let response  = await fetch('http://localhost:8000/auth/registration/', {
            method: 'POST',
            body: JSON.stringify({
                username: "Kate1",
                password: "Capsula1337",
                email: "ivanova.k@milandr.ru",
                first_name: "Ekaterina",
                last_name: "Ivanova"
            })
        });

        const myJson = await response.json();
        return 'ok';
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
                url: '/library/swaps/',
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
                    <button  onClick={() => this.handleSubmitRegistration()}>Registration</button>
            </Box>
        );
    }
}

export default HomePage;