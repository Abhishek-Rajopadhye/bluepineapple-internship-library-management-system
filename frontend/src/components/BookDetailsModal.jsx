import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';
import PropTypes from 'prop-types';

const BookDetailsModal = ({ open, onClose, book }) => {
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
            {/* Fetch and display allocations for the selected book */}
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
    name: PropTypes.string,
    author: PropTypes.string,
    total_copies: PropTypes.number,
    allocated_copies: PropTypes.number,
  }),
};

export { BookDetailsModal };