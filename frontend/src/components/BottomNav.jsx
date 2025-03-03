import { BottomNavigation, BottomNavigationAction } from '@mui/material';
import { Book as BookIcon, People as PeopleIcon } from '@mui/icons-material';
import PropTypes from 'prop-types';

const BottomNav = ({ value, setValue }) => {
  return (
    <BottomNavigation
      value={value}
      onChange={(event, newValue) => {
        setValue(newValue);
      }}
      showLabels
      className="BottomNavigation"
    >
      <BottomNavigationAction 
        label="Books" 
        icon={<BookIcon />} 
        onClick={() => {
          setValue(0);
          window.location.href = '/books';
        }} 
      />
      <BottomNavigationAction 
        label="Members" 
        icon={<PeopleIcon />} 
        onClick={() => {
          setValue(1);
          window.location.href = '/members';
        }} 
      />
    </BottomNavigation>
  );
};

BottomNav.propTypes = {
    value: PropTypes.number.isRequired,
    setValue: PropTypes.func.isRequired,
};

export { BottomNav };
