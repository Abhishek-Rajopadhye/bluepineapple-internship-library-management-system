import { useEffect, useState } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, CircularProgress, Button } from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { MemberDetailsModal } from './MemberDetailsModal';
import { AddMemberModal } from './AddMemberModal';
import { EditMemberModal } from './EditMemberModal';

const Members = () => {
    const [members, setMembers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedMember, setSelectedMember] = useState(null);
    const [openDetails, setOpenDetails] = useState(false);
    const [openAdd, setOpenAdd] = useState(false);
    const [openEdit, setOpenEdit] = useState(false);
  
    useEffect(() => {
        const fetchMembers = async () => {
            try {
                const response = await fetch('http://localhost:8000/members/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setMembers(data);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };
    
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
            const response = await fetch('http://localhost:8000/members/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newMember),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const addedMember = await response.json();
            setMembers((prevMembers) => [...prevMembers, addedMember]);
        } catch (error) {
            setError(error.message);
        }
    };

    const handleEditMember = async (updatedMember) => {
        try {
            const response = await fetch(`http://localhost:8000/members/${updatedMember.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedMember),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const editedMember = await response.json();
            setMembers((prevMembers) =>
                prevMembers.map((member) => (member.id === editedMember.id ? editedMember : member))
            );
        } catch (error) {
            setError(error.message);
        }
    };
    
  
    const handleDeleteMember = async (memberId) => {
        try {
            const response = await fetch(`http://localhost:8000/members/${memberId}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            setMembers((prevMembers) => prevMembers.filter((member) => member.id !== memberId));
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
                        <TableCell>Number of Allocated Books</TableCell>
                        <TableCell>Actions</TableCell>
                    </TableRow>
                    </TableHead>
                    <TableBody>
                        {members.map((member) => (
                            <TableRow key={member.id} onClick={() => handleOpenDetails(member)} style={{ cursor: 'pointer' }}>
                                <TableCell>{member.name}</TableCell>
                                <TableCell>{member.email}</TableCell>
                                <TableCell>{member.phone}</TableCell>
                                <TableCell>{member.allocated_books}</TableCell>
                                <TableCell>
                                    <IconButton onClick={(e) => { e.stopPropagation(); handleOpenEdit(member); }}>
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton onClick={(e) => { e.stopPropagation(); handleDeleteMember(member.id); }}>
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