import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

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
    name: PropTypes.string,
    author: PropTypes.string,
    total_copies: PropTypes.number,
  }),
  onSave: PropTypes.func.isRequired,
};

export { EditBookModal };