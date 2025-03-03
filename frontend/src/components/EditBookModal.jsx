import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const EditBookModal = ({ open, onClose, book, onSave }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Edit Book</DialogTitle>
      <DialogContent>
        <TextField label="Name" fullWidth margin="normal" defaultValue={book?.name} />
        <TextField label="Author" fullWidth margin="normal" defaultValue={book?.author} />
        <TextField label="Total Copies" type="number" fullWidth margin="normal" defaultValue={book?.total_copies} />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={onSave} color="primary">
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