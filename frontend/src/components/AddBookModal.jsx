import { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const AddBookModal = ({ open, onClose, onAdd }) => {
    const [name, setName] = useState('');
    const [author, setAuthor] = useState('');
    const [totalCopies, setTotalCopies] = useState('');
  
    const handleAdd = () => {
        const newBook = {
            name,
            author,
            total_copies: parseInt(totalCopies, 10),
            allocated_copies: 0,
        };
        onAdd(newBook);
        onClose();
    };
  
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Add New Book</DialogTitle>
            <DialogContent>
                <TextField
                label="Name"
                fullWidth
                margin="normal"
                value={name}
                onChange={(e) => setName(e.target.value)}
                />
                <TextField
                label="Author"
                fullWidth
                margin="normal"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                />
                <TextField
                label="Total Copies"
                type="number"
                fullWidth
                margin="normal"
                value={totalCopies}
                onChange={(e) => setTotalCopies(e.target.value)}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose} color="primary">
                    Cancel
                </Button>
                <Button onClick={handleAdd} color="primary">
                    Add
                </Button>
            </DialogActions>
        </Dialog>
    );
};

AddBookModal.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onAdd: PropTypes.func.isRequired,
};

export { AddBookModal };
