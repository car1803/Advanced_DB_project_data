import { useState } from 'react';
import { Button, Container, Form, Row } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const SearcherComponent = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        let collectionName = '';

        // Determinar collectionName según el término de búsqueda ingresado
        switch (searchTerm.toLowerCase()) {
            case 'trabajo':
                collectionName = 'hregistrotrabajo';
                break;
            case 'empresa':
                collectionName = 'hregistroempresa';
                break;
            case 'idioma':
                collectionName = 'hregistroestudioidioma';
                break;
            default:
                console.error('Invalid search term');
                return;
        }

        // Redirigir a la página de la tabla con el collectionName correspondiente
        navigate(`/data-table/${collectionName}`);
    };

    return (
        <Container className='text-start'>
            <Row>
                <h1 className='m-4'>Buscador:</h1>
                <Form className='border p-4 rounded' onSubmit={handleSearch}>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Buscar:</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Escribe aquí lo que deseas buscar"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </Form.Group>
                    <Button variant="primary" type="submit">Buscar</Button>
                </Form>
            </Row>
        </Container>
    );
};

export default SearcherComponent;
