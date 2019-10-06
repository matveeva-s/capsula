import React from 'react';
import styles from './Book.module.css';


function Book(props) {
    return (
        <div className={styles.book}>
            <img src={props.img} className={styles.book_cover}></img>
            <h4 className={styles.book_title}>
                Book!
            </h4>
        </div>
    )
}

export default Book;