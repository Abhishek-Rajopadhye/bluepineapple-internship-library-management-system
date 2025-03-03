import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const AddBookModal = ({ open, onClose, onAdd }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Add New Book</DialogTitle>
      <DialogContent>
        <TextField label="Name" fullWidth margin="normal" />
        <TextField label="Author" fullWidth margin="normal" />
        <TextField label="Total Copies" type="number" fullWidth margin="normal" />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={onAdd} color="primary">
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
