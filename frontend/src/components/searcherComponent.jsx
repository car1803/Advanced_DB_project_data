import axios from 'axios';
import { useState, useEffect } from 'react';
import { Button, Container, Form, Row } from 'react-bootstrap';
import glovars  from '../glovars';

const SearcherComponent = ({ DataTableComponent, ModalComponent }) => {
    const [searchTerm, setSearchTerm]  = useState('');
    const [data, setData] = useState(null);
    const [collectionSelected, setCollectionSelected] = useState(null);
    const [collectionSelectedDummy, setCollectionSelectedDummy] = useState(null);
    const [showTable, setShowTable] = useState(false);
    const [ defaultSelectValue ] = useState('--Selecciona una colección--');
    const [ showModal, setShowModal ] = useState(false);
    const [ modalData ] = useState({ title: 'Error', description: 'Por favor, selecciona una colección y escribe un término de búsqueda' });

    useEffect(() => {
        let midata = ["Cargando..."];
        setData(midata);
        
        axios.get(`${glovars.backendUrl}/getCollections`).then((response) => {
            response.data.unshift(defaultSelectValue);
            setData(response.data);
        }).catch((error) => {
            console.error('Error fetching data:', error.message);
        });

        setShowTable(false);
      }, [defaultSelectValue]); 

    const handleSearch = (e) => {
        if (!searchTerm || !collectionSelectedDummy || collectionSelectedDummy === defaultSelectValue) {
            setShowModal(true);
            setShowTable(false);
            e.preventDefault();
            return;
        }
        setCollectionSelected(collectionSelectedDummy);
        setShowTable(true);
        e.preventDefault();
        console.log('Search term:', searchTerm);
        console.log('Collection selected:', collectionSelectedDummy);
    };

    return (
        <Container className ='text-start'>
            <Row>
                <h1 className='m-4'>Buscador:</h1>
                <Form className='border p-4 rounded is-invalid' onSubmit={handleSearch}>
                    <Form.Group className="mb-3" controlId="formBasicEmail">
                        <Form.Label>Buscar:</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="Escribe aquí lo que deseas buscar"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicPassword">
                        <Form.Select  
                            onChange={(e) => {if(e.target.value !== defaultSelectValue) return setCollectionSelectedDummy(e.target.value)}} className='mb-3 m-1'>
                            {data && data.map((item, index) => ( <option key={index} value={item}>{item}</option> ))}
                        </Form.Select>
                    </Form.Group>
                    
                    <Button variant="primary" type="submit">Buscar</Button>
                </Form>
            </Row>
            { showTable && 
                <Row>
                    <DataTableComponent collectionName = { collectionSelected } />
                </Row>
            }

            <ModalComponent setShowModal={setShowModal} show = {showModal} title = { modalData.title } description = { modalData.description } />
        </Container>
    );
};

export default SearcherComponent;
