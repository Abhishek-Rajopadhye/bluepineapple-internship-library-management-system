import { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const AllocateBookModal = ({ open, onClose, onAllocate }) => {
    const [memberId, setMemberId] = useState('');
    const [fromDate, setFromDate] = useState('');
    const [toDate, setToDate] = useState('');
  
    const handleAllocate = () => {
        const allocation = {
            member_id: parseInt(memberId, 10),
            start_date: fromDate,
            end_date: toDate,
        };
        onAllocate(allocation);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Allocate Book</DialogTitle>
            <DialogContent>
                <TextField
                label="Member ID"
                fullWidth
                margin="normal"
                value={memberId}
                onChange={(e) => setMemberId(e.target.value)}
                />
                <TextField
                label="From Date"
                type="date"
                fullWidth
                margin="normal"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                />
                <TextField
                label="To Date"
                type="date"
                fullWidth
                margin="normal"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Cancel
                </Button>
                <Button onClick={handleAllocate} color="primary">
                    Allocate
                </Button>
            </DialogActions>
        </Dialog>
      );
};

AllocateBookModal.propTypes = {
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onAllocate: PropTypes.func.isRequired,
};

export { AllocateBookModal };
