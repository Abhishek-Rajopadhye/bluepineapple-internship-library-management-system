import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, MenuItem } from '@mui/material';
import PropTypes from 'prop-types';

const AllocateBookModal = ({ open, onClose, onAllocate }) => {
  const [members, setMembers] = useState([]);
  const [memberId, setMemberId] = useState('');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  useEffect(() => {
    const fetchMembers = async () => {
      try {
        const response = await fetch('http://localhost:8000/members/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setMembers(data);
      } catch (error) {
        console.error('Error fetching members:', error);
      }
    };

    fetchMembers();
  }, []);

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
          select
          label="Member"
          fullWidth
          margin="normal"
          value={memberId}
          onChange={(event) => setMemberId(event.target.value)}
        >
          {members.map((member) => (
            <MenuItem key={member.id} value={member.id}>
              {member.name}
            </MenuItem>
          ))}
        </TextField>
        <TextField
          label="From Date"
          type="date"
          fullWidth
          margin="normal"
          slotProps={{ inputLabel: { shrink: true } }}
          value={fromDate}
          onChange={(event) => setFromDate(event.target.value)}
        />
        <TextField
          label="To Date"
          type="date"
          fullWidth
          margin="normal"
          slotProps={{ inputLabel: { shrink: true } }}
          value={toDate}
          onChange={(event) => setToDate(event.target.value)}
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
