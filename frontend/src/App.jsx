import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AppBar, Toolbar, Typography, InputBase, BottomNavigation, BottomNavigationAction, Container } from '@mui/material';
import { Search as SearchIcon, Book as BookIcon, People as PeopleIcon } from '@mui/icons-material';
import { Books } from './components/Books';
import { Members } from './components/Members';
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [value, setValue] = useState(0);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

return (
    <Router>
        <AppBar position="static">
            <Toolbar>
                <Typography noWrap variant="h6" component="div" sx={{ flexGrow: 1 }} >
                    Library Management System
                </Typography>
                <div style={{ flexGrow: 1 }} />
                <div style={{ position: 'relative', borderRadius: '4px', backgroundColor: '#fff', marginLeft: 0, width: '100%' }}>
                    <div style={{ padding: '0 16px', height: '100%', position: 'absolute', pointerEvents: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <SearchIcon />
                    </div>
                    <InputBase
                        placeholder="Search…"
                        inputProps={{ 'aria-label': 'search' }}
                        style={{ color: 'inherit', paddingLeft: `calc(1em + 32px)`, width: '100%' }}
                        value={searchQuery}
                        onChange={handleSearchChange}
                    />
                </div>
            </Toolbar>
        </AppBar>
        <Container style={{ marginTop: '16px', marginBottom: '56px' }}>
            <Routes>
                <Route path="/books" element={<Books searchQuery={searchQuery} />} />
                <Route path="/members" element={<Members searchQuery={searchQuery} />} />
            </Routes>
        </Container>
        <BottomNavigation
            value={value}
            onChange={(event, newValue) => {
                setValue(newValue);
            }}
            showLabels
            style={{ position: 'fixed', bottom: 0, width: '100%' }}
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
    </Router>
);
}

export default App;
