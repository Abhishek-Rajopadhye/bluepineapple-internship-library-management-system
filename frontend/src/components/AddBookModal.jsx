/**
 * @file AddBookModal.jsx
 * @description This component provides a modal dialog for adding a new book.
 * @component
 * @name AddBookModal
 * @requires react
 * @requires @mui/material
 * @requires prop-types
 * @export AddBookModal
 */
import { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

/**
 * AddBookModal component that provides a modal dialog for adding a new book.
 * @component
 * @name AddBookModal
 * @param {Object} props - The component props.
 * @param {boolean} props.open - Indicates whether the modal is open.
 * @param {Function} props.onClose - Function to close the modal.
 * @param {Function} props.onAdd - Function to add a new book.
 * @returns {JSX.Element} The rendered AddBookModal component.
 */
const AddBookModal = ({ open, onClose, onAdd }) => {
    const [name, setName] = useState('');
    const [author, setAuthor] = useState('');
    const [totalCopies, setTotalCopies] = useState('');
  
    const handleAdd = () => {
        const newBook = {
            id:-1,
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
                onChange={(event) => setName(event.target.value)}
                />
                <TextField
                label="Author"
                fullWidth
                margin="normal"
                value={author}
                onChange={(event) => setAuthor(event.target.value)}
                />
                <TextField
                label="Total Copies"
                type="number"
                fullWidth
                margin="normal"
                value={totalCopies}
                onChange={(event) => setTotalCopies(event.target.value)}
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
