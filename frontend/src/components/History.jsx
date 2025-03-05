/**
 * @file History.jsx
 * @description This component displays a history of allocations of books.
 * @component
 * @name History
 * @requires react
 * @requires axios
 * @requires prop-types
 * @requires @mui/material
 * @requires @mui/icons-material
 * @export History
 */
import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress } from '@mui/material';

/**
 * History component that displays a history of allocations of books.
 * @component
 * @name History
 * @param {string} searchQuery - Query entered into the search bar.
 * @returns {JSX.Element} The rendered Books component.
 */
const History = ({ searchQuery }) => {
    const [history, setHistory] = useState([]);
    const [bookKey, setBookKey] = useState([]);
    const [memberKey, setMemberKey] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    const fetchHistory = async () => {
        try {
            const response = await fetch('http://localhost:8000/history/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setHistory(data.reverse());
            
            const bookPromises = {};
            const memberPromises = {};
                
            data.forEach(allocation => {
                if (!bookPromises[allocation.book_id]) {
                    bookPromises[allocation.book_id] = axios.get(`http://localhost:8000/books/${allocation.book_id}`);
                }
                if (!memberPromises[allocation.member_id]) {
                    memberPromises[allocation.member_id] = axios.get(`http://localhost:8000/members/${allocation.member_id}`);
                }
            });
            
            const bookResults = await Promise.all(Object.values(bookPromises));
            const memberResults = await Promise.all(Object.values(memberPromises));
            
            const booksData = {};
            const membersData = {};
            
            bookResults.forEach(res => booksData[res.data.id] = res.data.name);
            memberResults.forEach(res => membersData[res.data.id] = res.data.name);
            
            setBookKey(booksData);
            setMemberKey(membersData);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);
  
    if (loading) {
      return <CircularProgress />;
    }
  
    if (error) {
      return <Typography color="error">{error}</Typography>;
    }
  
    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                History
            </Typography>
            <TableContainer component={Paper} style={{ marginTop: '16px' }}>
            <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Book</TableCell>
                            <TableCell>Member</TableCell>
                            <TableCell>From</TableCell>
                            <TableCell>To</TableCell>
                            <TableCell>Returned</TableCell>
                            <TableCell>Overdue</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {history.filter(allocation => bookKey[allocation.book_id]?.toLowerCase().includes(searchQuery)).map((allocation) => (
                            <TableRow key={allocation.id}>
                                <TableCell>{bookKey[allocation.book_id] || 'Loading...'}</TableCell>
                                <TableCell>{memberKey[allocation.member_id] || 'Loading...'}</TableCell>
                                <TableCell>{allocation.start_date}</TableCell>
                                <TableCell>{allocation.end_date}</TableCell>
                                <TableCell>{allocation.returned ? 'Yes' : 'No'}</TableCell>
                                <TableCell>{allocation.overdue ? 'Yes' : 'No'}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>  
        </Container>
    );
};

History.propTypes = {
    searchQuery: PropTypes.string.isRequired,
};

export { History };
