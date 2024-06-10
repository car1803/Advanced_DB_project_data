import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, Pagination, FormControl, InputGroup, Button, Alert } from 'react-bootstrap';
import MetabaseComponent from './metabaseComponent';

function isObject(value) {
  return value !== null && typeof value === 'object';
}

function tooLong(text, maxLength) {
  text = text.toString();
  return text.length > maxLength;
}

function spamConNegrillaEnPalabras(texto, palabras) {
  texto = texto.toString();

  let palabrasValidas = [];

  for (var i = 0; i < palabras.length; i++) {
    let palabra = palabras[i];
    palabra = palabra.replace(/[*+.\s$-]/g, '');
    if (palabra.length > 0) {
      palabrasValidas.push(palabra);
    }
  }

  palabras = palabrasValidas;

  for (var j = 0; j < palabras.length; j++) {
    let palabra = palabras[j];
    texto = texto.replace(new RegExp(palabra, "gi"), "<spam style = 'font-weight: bold; color: red;'>" + palabra + "</spam>");
  }

  return <span dangerouslySetInnerHTML={{ __html: texto }} />;
}

const DataTableComponent = ({ collectionName, itemsPerPage, searchTerm, ModalComponent }) => {
  const [, setSearchTerm] = useState('');
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [filteredData, setFilteredData] = useState([]);
  const [modalData, setModalData] = useState({ title: '', description: '' });
  const [showModal, setShowModal] = useState(false);
  const [queryTime, setQueryTime] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/${collectionName}`, {
          params: { query: searchTerm }
        });
        setData(response.data.documents);
        setQueryTime(response.data.queryTime);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchData();
  }, [collectionName, searchTerm, currentPage]);

  useEffect(() => {
    setFilteredData(data);
  }, [data]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (data.length === 0) {
    return <div>Loading...</div>;
  }

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const metabaseCollectionsDictionary = {
    "salario_promedio_por_sector": "http://localhost:3300/public/question/b7aa9d8b-017d-408d-86c3-fa290383b304", 
    "salario_promedio_por_pais": "http://localhost:3300/public/question/57dbec53-6cb2-46d8-bfe5-c4259871c5a8", 
    "salario_promedio_por_genero": "http://localhost:3300/public/question/b499066b-448f-4e22-92b8-102e3504ab96",
    "salario_promedio_por_cargo": "http://localhost:3300/public/question/ddee8620-fa18-41fb-9f07-9ccf85d1e56a",
    "promedio_nivel_por_idioma": "http://localhost:3300/public/question/42d9f256-6fe2-4534-bd89-d8e7b117df4f", 
    "promedio_gasto_salarios_por_sector": "http://localhost:3300/public/question/f9d5de18-470a-4174-a290-a5ef791e4d40", 
    "palabras_mas_comunes_en_cargos":"http://localhost:3300/public/question/313fcf2e-e214-49ce-922d-ec9bf2bd7257",
    "nombre_empresas_mas_frecuente":"http://localhost:3300/public/question/ccf2ac9d-928a-414c-9725-a53026b7c6dc",
    "niveles_idioma_mas_comunes":"http://localhost:3300/public/question/63710329-e80c-45a2-b2fd-aeb35c0cdb2f",
    "estudiantes_por_pais":"http://localhost:3300/public/question/b27a5211-335c-4767-bb6d-235994bd84d2",
    "estudiantes_por_genero":"http://localhost:3300/public/question/ccba0e94-db79-4cb2-9087-3a2e0adf25d6",
    "empresa_por_tipo":"http://localhost:3300/public/question/aa61ff0c-10be-4040-a6c1-8b8a3310a44c",
    "edad_promedio_egresados":"http://localhost:3300/public/question/0703316f-4e9e-4be0-a35a-fa0ca6e06f2d",  
    "carreras_mas_comunes_en_empresas":"http://localhost:3300/public/question/e3b4d9f5-ffd9-489c-a27a-9c018368c5d1", 
    "cantidad_personas_por_genero_y_sector":"http://localhost:3300/public/question/f3f50bec-d6e6-4806-95ca-41896fdd61be",
    "cantidad_estudiantes_por_idioma":"http://localhost:3300/public/question/3a9c7750-1704-4197-a043-7ebfa98fcbb6",
  }

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const displayedData = filteredData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className='mb-3 p-3'>
      <InputGroup>
        <FormControl
          placeholder="Buscar"
          aria-label="Buscar"
          aria-describedby="basic-addon2"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </InputGroup>
      <ModalComponent title={modalData.title} description={modalData.description} show={showModal} setShowModal={setShowModal} />
      <MetabaseComponent src={metabaseCollectionsDictionary[collectionName] || null} onlyIframe={true}/>
      <div style={{ "overflow-x": "auto", "border": "2px solid #ccc"}}>
        <Table style={{ "white-space": "nowrap" }} striped bordered hover>
          <thead>
            <tr>
              {data && data.length > 0 && Object.keys(data[0]).map((key) => (
                <th className='text-capitalize text-center text-white bg-dark' key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayedData.map((item, index) => (
              <tr key={index}>
                {Object.values(item).map((val, i) => (
                  <td key={i}> {
                    isObject(val) ?
                      <Button
                        onClick={() => { setModalData({ title: Object.keys(data[0])[i], description: JSON.stringify(val) }); setShowModal(true); }}>Ver lista
                      </Button>
                    :
                      tooLong(val, 50) ?
                        <a href='/#' onClick={() => { setModalData({ title: Object.keys(data[0])[i], description: spamConNegrillaEnPalabras(val, searchTerm.split(' ')) }); setShowModal(true); }}>Ver...
                        </a>
                      :
                        spamConNegrillaEnPalabras(val, searchTerm.split(' '))
                    }
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
      <Pagination>
        {[...Array(totalPages).keys()].map((page) => (
          <Pagination.Item
            key={page + 1}
            active={page + 1 === currentPage}
            onClick={() => handlePageChange(page + 1)}
          >
            {page + 1}
          </Pagination.Item>
        ))}
      </Pagination>
      <Alert variant="info">
        Tiempo de consulta: {queryTime} ms
      </Alert>
    </div>
  );
};

export default DataTableComponent;
