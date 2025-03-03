import { useEffect, useState } from 'react';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, CircularProgress, Button } from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon, Assignment as AssignmentIcon } from '@mui/icons-material';
import { BookDetailsModal } from './BookDetailsModal';
import { AddBookModal } from './AddBookModal';
import { EditBookModal } from './EditBookModal';
import { AllocateBookModal } from './AllocateBookModal';

const Books = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBook, setSelectedBook] = useState(null);
  const [openDetails, setOpenDetails] = useState(false);
  const [openAdd, setOpenAdd] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [openAllocate, setOpenAllocate] = useState(false);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch('http://localhost:8000/books/');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setBooks(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  const handleOpenDetails = (book) => {
    setSelectedBook(book);
    setOpenDetails(true);
  };

  const handleCloseDetails = () => {
    setOpenDetails(false);
    setSelectedBook(null);
  };

  const handleOpenAdd = () => {
    setOpenAdd(true);
  };

  const handleCloseAdd = () => {
    setOpenAdd(false);
  };

  const handleOpenEdit = (book) => {
    setSelectedBook(book);
    setOpenEdit(true);
  };

  const handleCloseEdit = () => {
    setOpenEdit(false);
    setSelectedBook(null);
  };

  const handleOpenAllocate = (book) => {
    setSelectedBook(book);
    setOpenAllocate(true);
  };

  const handleCloseAllocate = () => {
    setOpenAllocate(false);
    setSelectedBook(null);
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Books
      </Typography>
      <Button variant="contained" color="primary" startIcon={<AddIcon />} onClick={handleOpenAdd}>
        Add New Book
      </Button>
      <TableContainer component={Paper} style={{ marginTop: '16px' }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Author</TableCell>
              <TableCell>Total Copies</TableCell>
              <TableCell>Allocated Copies</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {books.map((book) => (
              <TableRow key={book.id} onClick={() => handleOpenDetails(book)} style={{ cursor: 'pointer' }}>
                <TableCell>{book.name}</TableCell>
                <TableCell>{book.author}</TableCell>
                <TableCell>{book.total_copies}</TableCell>
                <TableCell>{book.allocated_copies}</TableCell>
                <TableCell>
                  <IconButton onClick={(e) => { e.stopPropagation(); handleOpenEdit(book); }}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={(e) => { e.stopPropagation(); /* Add delete functionality here */ }}>
                    <DeleteIcon />
                  </IconButton>
                  <IconButton onClick={(e) => { e.stopPropagation(); handleOpenAllocate(book); }}>
                    <AssignmentIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <BookDetailsModal open={openDetails} onClose={handleCloseDetails} book={selectedBook} />
      <AddBookModal open={openAdd} onClose={handleCloseAdd} onAdd={() => { /* Add book functionality here */ }} />
      <EditBookModal open={openEdit} onClose={handleCloseEdit} book={selectedBook} onSave={() => { /* Edit book functionality here */ }} />
      <AllocateBookModal open={openAllocate} onClose={handleCloseAllocate} onAllocate={() => { /* Allocate book functionality here */ }} />
    </Container>
  );
};

export { Books };