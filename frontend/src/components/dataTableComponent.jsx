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
    "salario_promedio_por_sector": "http://localhost:3300/public/question/19f8095f-153d-4333-9cb8-ec7ae876d8f3", 
    "salario_promedio_por_pais": "http://localhost:3300/public/question/fa1faa8a-4734-43d8-bd37-e78b051cc2cf", 
    "salario_promedio_por_genero": "http://localhost:3300/public/question/5bdd4288-f222-4595-b024-5f2a9ead3e0e",
    "salario_promedio_por_cargo": "http://localhost:3300/public/question/6907bb79-6a74-4712-91d9-50c53de3b1b8",
    "promedio_nivel_por_idioma": "http://localhost:3300/public/question/bb1d72a6-cdd2-452b-a4ee-eea20630401b", 
    "promedio_gasto_salarios_por_sector": "http://localhost:3300/public/question/19f8095f-153d-4333-9cb8-ec7ae876d8f3", 
    "palabras_mas_comunes_en_cargos":"http://localhost:3300/public/question/bb1d72a6-cdd2-452b-a4ee-eea20630401b",
    "nombre_empresas_mas_frecuente":"http://localhost:3300/public/question/235d6438-8440-48a0-a217-a203701d62bc",
    "niveles_idioma_mas_comunes":"http://localhost:3300/public/question/e7b6a07f-764d-4a7d-9947-0fcb9f22f44d",
    "estudiantes_por_pais":"http://localhost:3300/public/question/b33411f5-e33d-49d6-b549-8ea0d847fa3f",
    "estudiantes_por_genero":"http://localhost:3300/public/question/5d048564-05b0-47ee-9d1c-4f7405cbb039",
    "empresa_por_tipo":"http://localhost:3300/public/question/e4a7559d-2c80-4915-aaa0-8228b4e91f9f",
    "edad_promedio_egresados":"http://localhost:3300/public/question/373aa53d-8407-478f-904a-f2acde8b01a5",  
    "carreras_mas_comunes_en_empresas":"http://localhost:3300/public/question/ec7c0b1e-7fd8-4b71-8497-3f165c6cb20a", 
    "cantidad_personas_por_genero_y_sector":"http://localhost:3300/public/question/a1d98273-ccb6-4887-8aa8-76efc7d7097d",
    "cantidad_estudiantes_por_idioma":"http://localhost:3300/public/question/0f2e30df-c8e6-42aa-8cf6-ecf66ded2af3",
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
