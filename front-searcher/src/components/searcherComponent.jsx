import { Button, Container, Form, Row } from 'react-bootstrap';

const SearcherComponent = () => {
    return (
        <Container className='text-start'>
            <Row>
                <h1 className='m-4'>Buscador:</h1>
                <Form className='border p-4 rounded'>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Buscar:</Form.Label>
                    <Form.Control type="text" placeholder="Escribe aquí lo que deseas buscar" />
                    </Form.Group>
                    <Button variant="primary" type="submit">Buscar</Button>
                </Form>
            </Row>
        </Container>
    );
}

export default SearcherComponent;