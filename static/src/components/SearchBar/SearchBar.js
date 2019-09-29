import React, { createRef, Component } from 'react';
import { Search } from "grommet-icons";
import { 
    Box, 
    Image, 
    Text, 
    TextInput 
} from "grommet";


class SearchBar extends Component {
    state = { value: "", suggestionOpen: false, suggestedList: [] };

    boxRef = createRef();
  
    componentDidMount() {
        this.forceUpdate();
    }
  
    onChange = event => this.setState({ value: event.target.value }, () => {
        const { value } = this.state;
        if (!value.trim()) {
            this.setState({ suggestedList: [] });
        } else {
            // simulate an async call to the backend
            setTimeout(() => this.setState({ suggestedList: [] }), 300);
        }
    });
  
    onSelect = event => this.setState({ value: event.suggestion.value });
  
    renderSuggestions = () => {
        const { value, suggestedList } = this.state;
  
        return suggestedList
            .filter(
                ({ name }) => name.toLowerCase().indexOf(value.toLowerCase()) >= 0
            )
            .map(({ name, imageUrl }, index, list) => ({
                label: (
                    <Box
                        direction="row"
                        align="center"
                        gap="small"
                        border={index < list.length - 1 ? "bottom" : undefined}
                        pad="small"
                    >
                        <Image
                                width="48px"
                                src={imageUrl}
                                style={{ borderRadius: "100%" }}
                        />
                        <Text>
                                <strong>{name}</strong>
                        </Text>
                    </Box>
                ),
                value: name
            }));
    };
  
    render() {
        const { suggestionOpen, value } = this.state;
        return (
            <Box
                background="brand"
                ref={this.boxRef}
                width="40%"
                direction="row"
                align="center"
                pad={{ horizontal: "small", vertical: "xsmall" }}
                margin={{ horizontal: "small", vertical: "xsmall" }}
                round="small"
                elevation={suggestionOpen ? "medium" : undefined}
                border={{
                    side: "all",
                    color: suggestionOpen ? "transparent" : "border"
                }}
                style={
                    suggestionOpen
                    ? {
                        borderBottomLeftRadius: "0px",
                        borderBottomRightRadius: "0px"
                        }
                    : undefined
                }
            >
                <Search color="accent" />
                <TextInput
                    type="search"
                    dropTarget={this.boxRef.current}
                    plain
                    value={value}
                    onChange={this.onChange}
                    onSelect={this.onSelect}
                    suggestions={this.renderSuggestions()}
                    placeholder="Enter your name..."
                    onSuggestionsOpen={() => this.setState({ suggestionOpen: true })}
                    onSuggestionsClose={() =>
                    this.setState({ suggestionOpen: false })
                    }
                />
            </Box>
        );
    }
}

export default SearchBar;