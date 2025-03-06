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
 * @requires ./componenets/History
 * @requires ./components/TopBar
 * @requires ./components/BottomNav
 * @export App
 */
import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Container } from '@mui/material';
import { Books } from './components/Books';
import { Members } from './components/Members';
import { History } from './components/History';
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
        <>
        <Router>
            <TopBar searchQuery={searchQuery} handleSearchChange={handleSearchChange} />
            <Container className="Container">
                <Routes>
                    <Route path="/" element={<Navigate to="/books" />} />
                    <Route path="/books" element={<Books searchQuery={searchQuery} />} />
                    <Route path="/members" element={<Members searchQuery={searchQuery} />} />
                    <Route path="/history" element={<History searchQuery={searchQuery} />} />
                </Routes>
            </Container>
        </Router>
        <BottomNav/>
        </>
    );
}

export default App;