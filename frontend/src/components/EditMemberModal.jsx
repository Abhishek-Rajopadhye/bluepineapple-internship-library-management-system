/**
 * @file EditMemberModal.jsx
 * @description This component provides a modal dialog for editing member details.
 * @component
 * @name EditMemberModal
 * @requires react
 * @requires axios
 * @requires @mui/material
 * @requires prop-types
 * @export EditMemberModal
 */
import { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField } from '@mui/material';
import PropTypes from 'prop-types';

/**
 * EditMemberModal component that provides a modal dialog for editing member details.
 * @component
 * @name EditMemberModal
 * @param {Object} props - The component props.
 * @param {boolean} props.open - Indicates whether the modal is open.
 * @param {Function} props.onClose - Function to close
 * @param {Object} props.member - The member details.
 * @param {number} props.member.id - The member ID.
 * @param {string} props.member.name - The member name.
 * @param {string} props.member.email - The member email.
 * @param {number} props.member.phone - The member phone.
 * @param {Function} props.onSave - Function to edit the member.
 * @returns {JSX.Element} The rendered EditMemberModal component.
 */
const EditMemberModal = ({ open, onClose, member, onSave }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
  
    useEffect(() => {
        if (member) {
            setName(member.name);
            setEmail(member.email);
            setPhone(member.phone);
        }
    }, [member]);
  
    const handleSave = () => {
        const updatedMember = {
            ...member,
            name,
            email,
            phone,
        };
        onSave(updatedMember);
        onClose();
    };
  
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Edit Member</DialogTitle>
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
                <Button onClick={handleSave} color="primary">
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
