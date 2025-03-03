import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from '@mui/material';
import { Books } from './components/Books';
import { Members } from './components/Members';
import { TopBar } from './components/TopBar';
import { BottomNav } from './components/BottomNav';
import './App.css';

function App() {
    const [searchQuery, setSearchQuery] = useState('');
    const [value, setValue] = useState(0);
    const [location, setLocation] = useState("books")

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