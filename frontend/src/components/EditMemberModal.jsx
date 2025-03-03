import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

const EditMemberModal = ({ open, onClose, member, onSave }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Edit Member</DialogTitle>
      <DialogContent>
        <TextField label="Name" fullWidth margin="normal" defaultValue={member?.name} />
        <TextField label="Email" fullWidth margin="normal" defaultValue={member?.email} />
        <TextField label="Phone Number" fullWidth margin="normal" defaultValue={member?.phone} />
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

EditMemberModal.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  member: PropTypes.shape({
    name: PropTypes.string,
    email: PropTypes.string,
    phone: PropTypes.string,
  }),
  onSave: PropTypes.func.isRequired,
};

export { EditMemberModal };
