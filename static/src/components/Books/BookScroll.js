import React, { Component } from 'react';
import styles from './Book.module.css';
import { Box } from 'grommet';
import Book from './Book';
import { FormNext, FormPrevious } from 'grommet-icons';

class Scroll extends Component {
    state = { viewObjectsList: [] };
    componentDidMount() {
        this.setState({ viewObjectsList: [
            {title: '', coverage: 'https://i.pinimg.com/564x/2e/54/46/2e544650aba4d5fe2ed0be08bdc32b23.jpg', id: 1 },
            {title: '', coverage: 'https://i.pinimg.com/564x/2e/54/46/2e544650aba4d5fe2ed0be08bdc32b23.jpg', id: 2 },
            {title: '', coverage: 'https://i.pinimg.com/564x/2e/54/46/2e544650aba4d5fe2ed0be08bdc32b23.jpg', id: 3 },
            {title: '', coverage: 'https://i.pinimg.com/564x/2e/54/46/2e544650aba4d5fe2ed0be08bdc32b23.jpg', id: 4 }
        ] })
    }

    onArrowClick = (direction) => {
        if (direction === 'forward') {
            console.log(direction);
            this.setState({viewObjectsList: [
                {title: '', coverage: 'https://i.pinimg.com/564x/74/26/f8/7426f8bdf968010ad4daa520c2a1cfd7.jpg', id: 1 },
                {title: '', coverage: 'https://i.pinimg.com/564x/74/26/f8/7426f8bdf968010ad4daa520c2a1cfd7.jpg', id: 2 },
                {title: '', coverage: 'https://i.pinimg.com/564x/74/26/f8/7426f8bdf968010ad4daa520c2a1cfd7.jpg', id: 3 },
                {title: '', coverage: 'https://i.pinimg.com/564x/74/26/f8/7426f8bdf968010ad4daa520c2a1cfd7.jpg', id: 4 }
            ]});

        } else {
            this.setState({img: 'https://i.pinimg.com/564x/2e/54/46/2e544650aba4d5fe2ed0be08bdc32b23.jpg'})
        }
    }

    render(props) {
        return(
            <Box direction='column' align='center' className={styles.scroll_container}>
                <h3 className={styles.header}>{this.props.header}</h3>
                <Box background='background' direction='column' align='center'>
                    <Box 
                        flex 
                        pad='10px' 
                        direction='row' 
                        justify='around' 
                        gap='small' 
                        align='center'
                        >
                        <FormPrevious color='contrast' onClick={() => this.onArrowClick('back')} className={styles.arrow}></FormPrevious>
                        {this.state.viewObjectsList.map(({title, coverage, id}) => {
                            return(<Book img={coverage} key={id}></Book>)
                        })}
                        <FormNext color='contrast' onClick={() => this.onArrowClick('forward')} className={styles.arrow}></FormNext>
                    </Box>
                    <p className={styles.text}>See all</p>
                </Box>
            </Box>
        );
    }
}

export default Scroll;