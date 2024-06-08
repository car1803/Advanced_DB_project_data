import axios from 'axios';
import { useState, useEffect } from 'react';
import { Button, Container, Form, Row } from 'react-bootstrap';
import glovars from '../glovars';
import Select from 'react-select';

const SearcherComponent = ({ DataTableComponent, ModalComponent }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [data, setData] = useState(null);
    const [collectionSelected, setCollectionSelected] = useState(null);
    const [collectionSelectedDummy, setCollectionSelectedDummy] = useState(null);
    const [showTable, setShowTable] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [modalData] = useState({ title: 'Error', description: 'Por favor, selecciona una colección y escribe un término de búsqueda' });

    useEffect(() => {
        let midata = ["Cargando..."];
        setData(midata);

        axios.get(`${glovars.backendUrl}/getCollections`).then((response) => {
            setData(response.data);
        }).catch((error) => {
            console.error('Error fetching data:', error.message);
        });

        setShowTable(false);
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (!collectionSelectedDummy) {
            setShowModal(true);
            setShowTable(false);
            return;
        }
        if (collectionSelectedDummy.startsWith('h') && !searchTerm) {
            setShowModal(true);
            setShowTable(false);
            return;
        }
        
        const effectiveSearchTerm = collectionSelectedDummy.startsWith('h') ? searchTerm : '-';
        setSearchTerm(effectiveSearchTerm);
        setCollectionSelected(collectionSelectedDummy);
        setShowTable(true);
    };

    const groupedOptions = data && [
        {
            label: 'Colecciones de hecho, RI habilitado.',
            options: data.filter(item => item.toLowerCase().startsWith('h')).map(item => ({ value: item, label: item }))
        },
        {
            label: 'Otras colecciones.',
            options: data.filter(item => !item.toLowerCase().startsWith('h')).map(item => ({ value: item, label: item }))
        }
    ];

    return (
        <Container className='text-start'>
            <Row>
                <h1 className='m-4'>Buscador:</h1>
                <Form className='border p-4 rounded is-invalid' onSubmit={handleSearch}>
                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Select
                            options={groupedOptions}
                            onChange={(e) => setCollectionSelectedDummy(e.value)}
                            placeholder="--Selecciona una colección--"
                        />
                    </Form.Group>
                    {collectionSelectedDummy && collectionSelectedDummy.startsWith('h') && (
                        <Form.Group className="mb-3" controlId="formBasicEmail">
                            <Form.Label>Buscar:</Form.Label>
                            <Form.Control
                                type="text"
                                placeholder="Escribe aquí lo que deseas buscar"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </Form.Group>
                    )}
                    <Button variant="primary" type="submit">Buscar</Button>
                </Form>
            </Row>
            {showTable &&
                <Row>
                    <DataTableComponent collectionName={collectionSelected} searchTerm={searchTerm} ModalComponent={ModalComponent} itemsPerPage={10} />
                </Row>
            }

            <ModalComponent setShowModal={setShowModal} show={showModal} title={modalData.title} description={modalData.description} />
        </Container>
    );
};

export default SearcherComponent;
