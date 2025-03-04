/**
 * @file EditBookModal.jsx
 * @description This component provides a modal dialog for editing book details.
 * @component
 * @name EditbookModal
 * @requires react
 * @requires @mui/material
 * @requires prop-types
 * @export EditbookModal
 */
import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

/**
 * EditBookModal component that provides a modal dialog for editing book details.
 * @component
 * @name EditBookModal
 * @param {Object} props - The component props.
 * @param {boolean} props.open - Indicates whether the modal is open.
 * @param {Function} props.onClose - Function to close the modal.
 * @param {Object} props.book - The book object to edit.
 * @param {number} props.book.id - The book ID.
 * @param {string} props.book.name - The book name.
 * @param {string} props.book.author - The book author.
 * @param {number} props.book.total_copies - The total number of copies.
 * @param {number} props.book.allocated_copies - The number of allocated copies.
 * @param {Function} props.onSave - Function to edit the book.
 * @returns {JSX.Element} The rendered AddBookModal component.
 */
const EditBookModal = ({ open, onClose, book, onSave }) => {
    const [name, setName] = useState('');
    const [author, setAuthor] = useState('');
    const [totalCopies, setTotalCopies] = useState('');
  
    useEffect(() => {
        if (book) {
            setName(book.name);
            setAuthor(book.author);
            setTotalCopies(book.total_copies);
        }
    }, [book]);
  
    const handleSave = () => {
        const updatedBook = {
            ...book,
            name,
            author,
            total_copies: parseInt(totalCopies, 10),
        };
        onSave(updatedBook);
        onClose();
    };
  
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Edit Book</DialogTitle>
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
            <Button onClick={handleSave} color="primary">
                Save
            </Button>
            </DialogActions>
        </Dialog>
    );
};  

EditBookModal.propTypes = {
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    book: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        author: PropTypes.string,
        total_copies: PropTypes.number,
    }),
    onSave: PropTypes.func.isRequired,
};

export { EditBookModal };