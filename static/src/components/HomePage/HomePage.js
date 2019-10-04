import React, { Component } from 'react';
import { Box } from 'grommet';

import MenuButton from './../Button/MenuButton';
import Banner from './../Banner/Banner';


export default class HomePage extends Component {
 //test axios todo delete
    async handleSubmit(){
        console.log('press');
       /* axios({
            method: 'POST',

            url: 'http://localhost:8000/auth/login/', //'http://localhost:8000/user/me/',
        //    headers: {'Authorization': 'Token 63ca849a4d2d22c9af3b4a2e2c921bc2a1581e24'}
            headers:{'Content-Type': 'application/json',
                'Accept': 'application/json'},
            body: {
                data: {
                    username: "Svetik",
                    password: "Capsula1337"
                }
            }
        })
            .then(function (response) {
                console.log(response)
            });
    };*/
        let response  = await fetch('http://localhost:8000/auth/login/', {
            method: 'POST',
            body: JSON.stringify({
                username: "Svetik",
                password: "Capsula1337"
            })
        });
        console.log(response.json());}



    render(){
        return (
            <Box>
                <Banner/>
                    <MenuButton label='button'/>
                    <button  onClick={this.handleSubmit}>Add user</button>
            </Box>
        );
    }
}