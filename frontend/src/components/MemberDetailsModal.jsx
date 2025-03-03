import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';
import PropTypes from 'prop-types';

const MemberDetailsModal = ({ open, onClose, member }) => {
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Member Details</DialogTitle>
      <DialogContent>
        {member && (
          <>
            <Typography variant="h6">{member.name}</Typography>
            <Typography variant="subtitle1">{member.email}</Typography>
            <Typography variant="body2">Phone Number: {member.phone}</Typography>
            <Typography variant="body2">Number of Allocated Books: {member.allocated_books}</Typography>
            <Typography variant="h6" style={{ marginTop: '16px' }}>Allocations</Typography>
            {/* Fetch and display allocations for the selected member */}
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

MemberDetailsModal.propTypes = {
  open: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  member: PropTypes.shape({
    name: PropTypes.string,
    email: PropTypes.string,
    phone: PropTypes.string,
    allocated_books: PropTypes.number,
  }),
};

export { MemberDetailsModal };