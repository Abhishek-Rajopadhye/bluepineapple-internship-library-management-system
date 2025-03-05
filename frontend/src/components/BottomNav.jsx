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
import { Book as BookIcon, People as PeopleIcon, History as HistoryIcon } from '@mui/icons-material';

/**
 * BottomNav component that provides navigation between Books and Members sections.
 * @component
 * @name BottomNav
 * @returns {JSX.Element} The rendered BottomNav component.
 */
const BottomNav = () => {
    return (
        <BottomNavigation
        value={localStorage.getItem("Location") == "books" ? 0 : (localStorage.getItem("Location") == "members" ? 1 : 2)}
        showLabels
        className="BottomNavigation"
        >
        <BottomNavigationAction 
            label="Books" 
            icon={<BookIcon color={localStorage.getItem("Location") == "books" ? "primary" : "disabled" } />} 
            onClick={() => {
            localStorage.setItem("Location", "books")
            window.location.href = '/books';
            }}
        />
        <BottomNavigationAction 
            label="Members" 
            icon={<PeopleIcon color={localStorage.getItem("Location") == "members" ? "primary" : "disabled" } />} 
            onClick={() => {
            localStorage.setItem("Location", "members")
            window.location.href = '/members';
            }} 
        />
        <BottomNavigationAction 
            label="History" 
            icon={<HistoryIcon color={localStorage.getItem("Location") == "history" ? "primary" : "disabled" } />} 
            onClick={() => {
            localStorage.setItem("Location", "history")
            window.location.href = '/history';
            }} 
        />
        </BottomNavigation>
    );
};

export { BottomNav };
