import { BottomNavigation, BottomNavigationAction } from '@mui/material';
import { Book as BookIcon, People as PeopleIcon } from '@mui/icons-material';
import PropTypes from 'prop-types';

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
