import { Carousel, Image, Box } from 'grommet';
import React, { Component } from 'react';

class Banner extends Component {
    render() {
        return (
            <Box
                height='600px'
                width='100%'
            >
                <Carousel fill  controls='selectors'>
                    <Image fit="cover" src="https://cdn-images-1.medium.com/max/2400/1*l6is9AD4ciAM1d5482m8iw.jpeg" />
                    <Image fit="cover" src="https://www.sftour1.com/wp-content/uploads/2018/08/golden-gate-fogged.jpg" />
                    <Image fit="cover" src="https://media.licdn.com/dms/image/C4D1BAQE0VoWGQ9cqQg/company-background_10000/0?e=2159024400&v=beta&t=dpV3ZE_SAe5bvJGoD19Rcw0zXGJy0yHJCN_0z_nPwFo" />
                </Carousel>
            </Box>
        )
    }
}

export default Banner;