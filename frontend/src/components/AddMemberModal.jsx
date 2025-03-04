/**
 * @file AddMemberModal.jsx
 * @description This component provides a modal dialog for adding a new member.
 * @component
 * @name AddMemberModal
 * @requires react
 * @requires @mui/material
 * @requires prop-types
 * @export AddMemberModal
 */
import { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

/**
 * AddMemberModal component that provides a modal dialog for adding a new member.
 * @component
 * @name AddMemberModal
 * @param {Object} props - The component props.
 * @param {boolean} props.open - Indicates whether the modal is open.
 * @param {Function} props.onClose - Function to close the modal.
 * @param {Function} props.onAdd - Function to add a new member.
 * @returns {JSX.Element} The rendered AddMemberModal component.
 */
const AddMemberModal = ({ open, onClose, onAdd }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
  
    const handleAdd = () => {
        const newMember = {
            id:-1,
            name,
            email,
            phone,
        };
        onAdd(newMember);
        onClose();
    };
  
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Add New Member</DialogTitle>
            <DialogContent>
                <TextField
                    label="Name"
                    fullWidth
                    margin="normal"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <TextField
                    label="Email"
                    fullWidth
                    margin="normal"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                    label="Phone Number"
                    fullWidth
                    margin="normal"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
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

AddMemberModal.propTypes = {
    open: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onAdd: PropTypes.func.isRequired,
};

export { AddMemberModal };
