import { useState, useEffect } from 'react';
import axios from 'axios';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, List, ListItem, ListItemText } from '@mui/material';
import PropTypes from 'prop-types';

const BookDetailsModal = ({ open, onClose, book }) => {
    const [allocations, setAllocations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (book) {
        const fetchAllocations = async () => {
            try {
            const response = await axios.get(`http://localhost:8000/allocations/?book=${book.id.toString()}`);
            if (response.status !== 200) {
                throw new Error('Network response was not ok');
            }
            const data = response.data;

            // Fetch member details for each allocation
            const allocationsWithMemberNames = await Promise.all(
                data.map(async (allocation) => {
                const memberResponse = await axios.get(`http://localhost:8000/members/${allocation.member_id}`);
                if (memberResponse.status !== 200) {
                    throw new Error('Network response was not ok');
                }
                return {
                    ...allocation,
                    member_name: memberResponse.data.name,
                };
                })
            );

            setAllocations(allocationsWithMemberNames);
            } catch (error) {
            setError(error.message);
            } finally {
            setLoading(false);
            }
        };

        fetchAllocations();
        }
    }, [book]);

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Book Details</DialogTitle>
            <DialogContent>
                {book && (
                <>
                    <Typography variant="h6">{book.name}</Typography>
                    <Typography variant="subtitle1">{book.author}</Typography>
                    <Typography variant="body2">Total Copies: {book.total_copies}</Typography>
                    <Typography variant="body2">Allocated Copies: {book.allocated_copies}</Typography>
                    <Typography variant="h6" style={{ marginTop: '16px' }}>Allocations</Typography>
                    {loading ? (
                    <Typography>Loading...</Typography>
                    ) : error ? (
                    <Typography color="error">{error}</Typography>
                    ) : (
                    <List>
                        {allocations.map((allocation) => (
                        <ListItem key={allocation.id}>
                            <ListItemText
                            primary={`Member: ${allocation.member_name}`}
                            secondary={`From: ${allocation.start_date} To: ${allocation.end_date}`}
                            />
                        </ListItem>
                        ))}
                    </List>
                    )}
                </>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Close
                </Button>
            </DialogActions>
        </Dialog>
    );
};

BookDetailsModal.propTypes = {
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    book: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string,
        author: PropTypes.string,
        total_copies: PropTypes.number,
        allocated_copies: PropTypes.number,
    }),
};

export { BookDetailsModal };