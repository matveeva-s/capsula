import React from "react";

import { Box, Button } from "grommet";
import { Edit, Catalog } from 'grommet-icons';

const MenuButton = props => (
    <Box align="center" pad="medium">
        <Button
            label={ props.label }
            onClick={() => {}}
            hoverIndicator="light-1"
        />
    </Box>
);

export default MenuButton;