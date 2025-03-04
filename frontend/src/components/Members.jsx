/**
 * @file Members.jsx
 * @description This component displays a list of members and provides functionalities to add, edit, and delete members.
 * @component
 * @name Members
 * @requires react
 * @requires axios
 * @requires @mui/material
 * @requires @mui/icons-material
 * @requires ./MemberDetailsModal
 * @requires ./AddMemberModal
 * @requires ./EditMemberModal
 * @export Members
 */
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, CircularProgress, Button } from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { MemberDetailsModal } from './MemberDetailsModal';
import { AddMemberModal } from './AddMemberModal';
import { EditMemberModal } from './EditMemberModal';

/**
 * Members component displays a list of members and provides functionalities to add, edit, and delete members.
 * @component
 * @name Members
 * @returns {JSX.Element} The rendered Members component.
 */
const Members = () => {
    const [members, setMembers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedMember, setSelectedMember] = useState(null);
    const [openDetails, setOpenDetails] = useState(false);
    const [openAdd, setOpenAdd] = useState(false);
    const [openEdit, setOpenEdit] = useState(false);
  
    const fetchMembers = async () => {
        try {
            const response = await axios.get('http://localhost:8000/members/');
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            const { data } = await axios.get('http://localhost:8000/members/');
            setMembers(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMembers();
    }, []);
  
    const handleOpenDetails = (member) => {
        setSelectedMember(member);
        setOpenDetails(true);
    };
  
    const handleCloseDetails = () => {
        setOpenDetails(false);
        setSelectedMember(null);
    };
  
    const handleOpenAdd = () => {
        setOpenAdd(true);
    };
  
    const handleCloseAdd = () => {
        setOpenAdd(false);
    };
  
    const handleOpenEdit = (member) => {
        setSelectedMember(member);
        setOpenEdit(true);
    };
  
    const handleCloseEdit = () => {
        setOpenEdit(false);
        setSelectedMember(null);
    };
  
    const handleAddMember = async (newMember) => {
        try {
            const response = await axios.post('http://localhost:8000/members/', newMember, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchMembers();
        } catch (error) {
            setError(error.message);
        }
    };

    const handleEditMember = async (updatedMember) => {
        try {
            const response = await axios.put(`http://localhost:8000/members/${updatedMember.id}`, updatedMember, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchMembers();
        } catch (error) {
            setError(error.message);
        }
    };
    
  
    const handleDeleteMember = async (memberId) => {
        try {
            const response = await axios.delete(`http://localhost:8000/members/${memberId}`);
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchMembers();
        } catch (error) {
            setError(error.message);
        }
    };
  
    if (loading) {
        return <CircularProgress />;
    }
  
    if (error) {
        return <Typography color="error">Error: {error}</Typography>;
    }
  
    return (
      <Container>
            <Typography variant="h4" gutterBottom>
                Members
            </Typography>
            <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpenAdd}>
                Add New Member
            </Button>
            <TableContainer component={Paper} style={{ marginTop: '16px' }}>
                <Table>
                    <TableHead>
                    <TableRow>
                        <TableCell>Name</TableCell>
                        <TableCell>Email</TableCell>
                        <TableCell>Phone Number</TableCell>
                        <TableCell>Actions</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                        {members.map((member) => (
                            <TableRow key={member.id} onClick={() => handleOpenDetails(member)} style={{ cursor: 'pointer' }}>
                                <TableCell>{member.name}</TableCell>
                                <TableCell>{member.email}</TableCell>
                                <TableCell>{member.phone}</TableCell>
                                <TableCell>
                                    <IconButton onClick={(event) => { event.stopPropagation(); handleOpenEdit(member); }}>
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton onClick={(event) => { event.stopPropagation(); handleDeleteMember(member.id); }}>
                                        <DeleteIcon />
                                    </IconButton>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
    
            <MemberDetailsModal open={openDetails} onClose={handleCloseDetails} member={selectedMember} />
            <AddMemberModal open={openAdd} onClose={handleCloseAdd} onAdd={handleAddMember} />
            <EditMemberModal open={openEdit} onClose={handleCloseEdit} member={selectedMember} onSave={handleEditMember} />
        </Container>
    );
};

export { Members };