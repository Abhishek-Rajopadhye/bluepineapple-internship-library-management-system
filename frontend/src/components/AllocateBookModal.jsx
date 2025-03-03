import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const AllocateBookModal = ({ open, onClose, onAllocate }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Allocate Book</DialogTitle>
      <DialogContent>
        <TextField label="Member ID" fullWidth margin="normal" />
        <TextField label="From Date" type="date" fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
        <TextField label="To Date" type="date" fullWidth margin="normal" InputLabelProps={{ shrink: true }} />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={onAllocate} color="primary">
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
