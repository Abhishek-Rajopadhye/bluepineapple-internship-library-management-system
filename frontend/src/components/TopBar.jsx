/**
 * @file TopBar.jsx
 * @description A top navigation bar component for the Library Management System.
 * It includes a search input field for filtering content dynamically.
 * @component
 * @name TopBar
 * @requires react
 * @requires @mui/material
 * @requires @mui/icons-material
 * @export TopBar
 */
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import PropTypes from 'prop-types';

/**
 * Styled component for the search container.
 */
const Search = styled('div')(({ theme }) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginLeft: 'auto',
    width: '45%',
}));

/**
 * Styled component for the search icon wrapper.
 */
const SearchIconWrapper = styled('div')(({ theme }) => ({
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
}));

/**
 * Styled component for the input field within the search bar.
 */
const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: 'inherit',
    width: '100%',
    '& .MuiInputBase-input': {
        padding: theme.spacing(1, 1, 1, 0),
        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create('width'),
        width: '100%',
    },
}));


/**
 * TopBar component that provides a navigation header with a search bar.
 * @component
 * @name TopBar
 * @param {Object} props - The component props.
 * @param {string} props.searchQuery - The current search query.
 * @param {Function} props.handleSearchChange - The function to handle search input changes.
 * @returns {JSX.Element} The rendered TopBar component.
 */
const TopBar = ({ searchQuery, handleSearchChange }) => {
    return (
        <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" className="AppBar">
            <Toolbar className="Toolbar">
                <Typography variant="h6" noWrap>
                    Library Management System
                </Typography>
                <Search>
                    <SearchIconWrapper>
                    <SearchIcon />
                    </SearchIconWrapper>
                    <StyledInputBase
                    placeholder="Search…"
                    inputProps={{ 'aria-label': 'search' }}
                    value={searchQuery}
                    onChange={handleSearchChange}
                    />
                </Search>
            </Toolbar>
        </AppBar>
        </Box>
    );
};

TopBar.propTypes = {
    searchQuery: PropTypes.string.isRequired,
    handleSearchChange: PropTypes.func.isRequired,
};

export { TopBar };