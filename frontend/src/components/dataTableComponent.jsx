import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, Pagination, FormControl, InputGroup, Button } from 'react-bootstrap';

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
    //verificar si la palabra contiene caracteres especiales usados para el regex y eliminarlos
    let palabra = palabras[i];
    palabra = palabra.replace(/[*+.\s$-]/g, '');
    if (palabra.length > 0){
      palabrasValidas.push(palabra);
    }
  }
  
  palabras = palabrasValidas;	


  for (var j = 0; j < palabras.length; j++) {
    let palabra = palabras[j];
    //TODO: Reemplazar sin regex es decir ignorando punto y asteristo
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

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/${collectionName}`, {
          params: { query: searchTerm }
        });
        //console.log(response.data, 'response', collectionName, searchTerm);
        setData(response.data);
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
    console.log(error);
  }

  if (data.length === 0) {
    return <div>Loading...</div>;
  }

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

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
      <div style={{ "overflow-x": "auto", "border": "2px solid #ccc"}}>
        <Table style={{ 
              "white-space": "nowrap"}} striped bordered hover>
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
                        <a href='/#' onClick={() => { setModalData({ title: Object.keys(data[0])[i], description:  spamConNegrillaEnPalabras(val, searchTerm.split(' ')) }); setShowModal(true); }}>Ver...
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
    </div>
  );
};

export default DataTableComponent;
