/**
 * @file MemberDetailsModal.jsx
 * @description This component provides a modal dialog for displaying member details and allocations.
 * @component
 * @name MemberDetailsModal
 * @requires react
 * @requires axios
 * @requires @mui/material
 * @requires prop-types
 * @export MemberDetailsModal
 */
import { useEffect, useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, List, ListItem, ListItemText, ListItemButton } from '@mui/material';
import PropTypes from 'prop-types';
import axios from 'axios';

/**
 * MemberDetailsModal component that provides a modal dialog for displaying member details and allocations.
 * @component
 * @name MemberDetailsModal
 * @param {Object} props - The component props.
 * @param {boolean} props.open - Indicates whether the modal is open.
 * @param {Function} props.onClose - Function to close
 * @param {Object} props.member - The member details.
 * @param {number} props.member.id - The member ID.
 * @param {string} props.member.name - The member name.
 * @param {string} props.member.email - The member email.
 * @param {number} props.member.phone - The member phone.
 * @returns {JSX.Element} The rendered MemberDetailsModal component.
 */
const MemberDetailsModal = ({ open, onClose, member }) => {
    const [allocations, setAllocations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (member) {
        const fetchAllocations = async () => {
            try {
            const response = await axios.get(`http://localhost:8000/allocations/?member=${member.id.toString()}`);
            if (response.status !== 200) {
                throw new Error('Network response was not ok');
            }
            const data = response.data;

            // Fetch book details for each allocation
            const allocationsWithBookNames = await Promise.all(
                data.map(async (allocation) => {
                const bookResponse = await axios.get(`http://localhost:8000/books/${allocation.book_id}`);
                if (bookResponse.status !== 200) {
                    throw new Error('Network response was not ok');
                }
                return {
                    ...allocation,
                    book_name: bookResponse.data.name,
                };
                })
            );

            setAllocations(allocationsWithBookNames);
            } catch (error) {
            setError(error.message);
            } finally {
            setLoading(false);
            }
        };

        fetchAllocations();
        }
    }, [member]);

    const handleDeAllocate = async (allocation_id) => {
        try {
            const response = await axios.delete(`http://localhost:8000/allocations/${allocation_id}`);
            if(response.status != 200){
                throw new Error("Network response was not ok.")
            }            
            console.log(response);
        } catch (error){
            console.log(error.message)
        }
    };
    
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
                        primary={`Book: ${allocation.book_name}`}
                        secondary={`From: ${allocation.start_date} To: ${allocation.end_date}`}
                        />
                        <ListItemText primary={`${allocation.overdue ? "Overdue" : "Not Overdue"}`}/>
                        <ListItemButton onClick={(event) => { event.stopPropagation(); handleDeAllocate(allocation.id); }}>
                            <Typography variant="button" gutterBottom sx={{ display: 'block' }}>
                                Return
                            </Typography>
                        </ListItemButton>
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