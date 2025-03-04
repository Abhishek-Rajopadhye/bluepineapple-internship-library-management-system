/**
 * @file Books.jsx
 * @description This component displays a list of books and provides functionalities to add, edit, allocate, and delete books.
 * @component
 * @name Books
 * @requires react
 * @requires axios
 * @requires @mui/material
 * @requires @mui/icons-material
 * @requires ./BookDetailsModal
 * @requires ./AddBookModal
 * @requires ./EditBookModal
 * @requires ./AllocateBookModal
 * @export Books
 */
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, IconButton, CircularProgress, Button } from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon, Assignment as AssignmentIcon } from '@mui/icons-material';
import { BookDetailsModal } from './BookDetailsModal';
import { AddBookModal } from './AddBookModal';
import { EditBookModal } from './EditBookModal';
import { AllocateBookModal } from './AllocateBookModal';

/**
 * Books component that displays a list of books and provides functionalities to add, edit, allocate, and delete books.
 * @component
 * @name Books
 * @returns {JSX.Element} The rendered Books component.
 */
const Books = () => {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedBook, setSelectedBook] = useState(null);
    const [openDetails, setOpenDetails] = useState(false);
    const [openAdd, setOpenAdd] = useState(false);
    const [openEdit, setOpenEdit] = useState(false);
    const [openAllocate, setOpenAllocate] = useState(false);
  
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

    useEffect(() => {
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
  
    const handleAddBook = async (newBook) => {
        try {
            const response = await axios.post('http://localhost:8000/books/', newBook, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchBooks();
        } catch (error) {
            setError(error.message);
        }
    };
  
    const handleEditBook = async (updatedBook) => {
        try {
            const response = await axios.put(`http://localhost:8000/books/${updatedBook.id}`, updatedBook, {
            headers: {
                'Content-Type': 'application/json',
            },
            });
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchBooks();
        } catch (error) {
            setError(error.message);
        }
    };
  
    const handleAllocateBook = async (allocation) => {
        try {
            const response = await axios.post('http://localhost:8000/allocations/', {
                ...allocation,
                id: -1,
                book_id: selectedBook.id,
            }, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchBooks();
        } catch (error) {
            setError(error.message);
        }
    };
  
    const handleDeleteBook = async (bookId) => {
        try {
            const response = await axios.delete(`http://localhost:8000/books/${bookId}`);
            if (response.status != 200) {
                throw new Error('Network response was not ok');
            }
            fetchBooks();
        } catch (error) {
            setError(error.message);
        }
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
                                <IconButton onClick={(event) => { event.stopPropagation(); handleOpenEdit(book); }}>
                                    <EditIcon />
                                </IconButton>
                                <IconButton onClick={(event) => { event.stopPropagation(); handleDeleteBook(book.id); }}>
                                    <DeleteIcon />
                                </IconButton>
                                <IconButton onClick={(event) => { event.stopPropagation(); handleOpenAllocate(book); }}>
                                    <AssignmentIcon />
                                </IconButton>
                            </TableCell>
                        </TableRow>
                    ))}
                    </TableBody>
                </Table>
            </TableContainer>  
            <BookDetailsModal open={openDetails} onClose={handleCloseDetails} book={selectedBook} />
            <AddBookModal open={openAdd} onClose={handleCloseAdd} onAdd={handleAddBook} />
            <EditBookModal open={openEdit} onClose={handleCloseEdit} book={selectedBook} onSave={handleEditBook} />
            <AllocateBookModal open={openAllocate} onClose={handleCloseAllocate} onAllocate={handleAllocateBook} />
        </Container>
    );
};

export { Books };