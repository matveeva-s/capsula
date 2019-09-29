import React, { Component } from "react";
import { Box } from "grommet";
import styles from "./UserProfile.module.css";
import { Link } from 'react-router-dom';
import Book from '../Books/Book'
import Scroll from '../Books/BookScroll'

class UserPage extends Component {
    render() {
        return (
            <Box direction='column' align='center' fill className={styles.profile}>
                <Box background='accent' className={styles.background} align='center'>
                    <img
                        alt="Remy Sharp"
                        src="https://cdn.dribbble.com/users/1253590/screenshots/7221280/media/03e0c431c9196bdb0d32bbe5b030918c.png"
                        className={styles.big_avatar}
                    />
                </Box>
                <h3 className={styles.header1}>CharlyLovegood</h3>
                <p className={styles.header2}>Ivanova Natalia</p>

                <Scroll header='My Books'></Scroll>
                <Scroll header='My Wishlist'></Scroll>
            </Box>
        )
    }
}

export default UserPage;