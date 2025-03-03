import { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, List, ListItem, ListItemText } from '@mui/material';
import PropTypes from 'prop-types';

const MemberDetailsModal = ({ open, onClose, member }) => {
    const [allocations, setAllocations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
        if (member) {
            const fetchAllocations = async () => {
            try {
                const response = await fetch(`http://localhost:8000/allocations/member=${member.id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setAllocations(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
            };
    
            fetchAllocations();
        }
    }, [member]);
  
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Member Details</DialogTitle>
            <DialogContent>
                {member && (
                    <>
                    <Typography variant="h6">{member.name}</Typography>
                    <Typography variant="subtitle1">{member.email}</Typography>
                    <Typography variant="body2">Phone Number: {member.phone}</Typography>
                    <Typography variant="body2">Number of Allocated Books: {allocations.length}</Typography>
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
                                primary={`Book ID: ${allocation.book_id}`}
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
  
MemberDetailsModal.propTypes = {
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    member: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        email: PropTypes.string,
        phone: PropTypes.string,
    }),
};

export { MemberDetailsModal };