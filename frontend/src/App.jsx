/**
 * @file App.jsx
 * @description This is the main entry point of the application, setting up routing and layout structure.
 * It includes a top navigation bar, dynamic content switching between Books and Members components,
 * and a bottom navigation bar for navigation control.
 * @component
 * @name App
 * @requires react
 * @requires react-router-dom
 * @requires @mui/material
 * @requires ./componenets/Books
 * @requires ./componenets/Members
 * @requires ./components/TopBar
 * @requires ./components/BottomNav
 * @export App
 */
import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from '@mui/material';
import { Books } from './components/Books';
import { Members } from './components/Members';
import { TopBar } from './components/TopBar';
import { BottomNav } from './components/BottomNav';
import './App.css';

/**
 * Main application component.
 * Manages the routing and layout of the application.
 * @component
 * @name App
 * @returns {JSX.Element} The rendered App component.
 */
function App() {
    const [searchQuery, setSearchQuery] = useState('');
    const [value, setValue] = useState(0);
    const [location, setLocation] = useState("books")

    /**
     * Handles search input changes and updates the search query state.
     * @function
     * @name handleSearchChange
     * @param {React.ChangeEvent<HTMLInputElement>} event - The event object from the input field.
     */
    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
    };

    return (
        <Router>
            <TopBar searchQuery={searchQuery} handleSearchChange={handleSearchChange} />
            <Container className="Container">
                <Routes>
                    <Route path="/books" element={<Books searchQuery={searchQuery} />} />
                    <Route path="/members" element={<Members searchQuery={searchQuery} />} />
                </Routes>
            </Container>
            <BottomNav value={value} setValue={setValue} location={location} setLocation={setLocation}/>
        </Router>
    );
}

export default App;