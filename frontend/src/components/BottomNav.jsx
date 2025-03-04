/**
 * @file BottomNav.jsx
 * @description A bottom navigation component for switching between Books and Members sections.
 * @component
 * @name BottomNav
 * @requires react
 * @requires @mui/material
 * @requires @mui/icons-material
 * @export BottomNav
 */
import { BottomNavigation, BottomNavigationAction } from '@mui/material';
import { Book as BookIcon, People as PeopleIcon } from '@mui/icons-material';
import PropTypes from 'prop-types';


/**
 * BottomNav component that provides navigation between Books and Members sections.
 * @component
 * @name BottomNav
 * @param {Object} props - The component props.
 * @param {number} props.value - The current selected navigation value.
 * @param {Function} props.setValue - The function to update the navigation value.
 * @param {string} props.location - The current location state.
 * @param {Function} props.setLocation - The function to update the location state.
 * @returns {JSX.Element} The rendered BottomNav component.
 */
const BottomNav = ({ value, setValue, location, setLocation }) => {
  return (
    <BottomNavigation
      value={value}
      showLabels
      className="BottomNavigation"
    >
      <BottomNavigationAction 
        label="Books" 
        icon={<BookIcon color={location == "books" ? "primary" : "disabled" } />} 
        onClick={() => {
          setValue(0);
          setLocation("books")
          window.location.href = '/books';
        }}
      />
      <BottomNavigationAction 
        label="Members" 
        icon={<PeopleIcon color={location == "members" ? "primary" : "disabled" } />} 
        onClick={() => {
          setValue(1);
          setLocation("members")
          window.location.href = '/members';
        }} 
      />
    </BottomNavigation>
  );
};

BottomNav.propTypes = {
    value: PropTypes.number.isRequired,
    setValue: PropTypes.func.isRequired,
    location: PropTypes.string.isRequired,
    setLocation: PropTypes.func.isRequired
};

export { BottomNav };
