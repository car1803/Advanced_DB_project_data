import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, Pagination, FormControl, InputGroup, Button } from 'react-bootstrap';

function isObject(value) {
  return value !== null && typeof value === 'object';
}

const DataTableComponent = ({ collectionName, itemsPerPage, ModalComponent }) => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredData, setFilteredData] = useState([]);
  const [modalData, setModalData] = useState({ title: '', description: '' });
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/${collectionName}`);
        setData(response.data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchData();
  }, [collectionName]);

  useEffect(() => {
    let resposeData = data.filter(item =>
      Object.values(item).some(
        val =>
          val
            .toString()
            .toLowerCase()
            .indexOf(searchTerm.toLowerCase()) !== -1
      )
    );
    
    setFilteredData(resposeData);
  }, [searchTerm, data]);

  if (error) {
    return <div>Error: {error}</div>;
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
      <Table striped bordered hover>
        <thead>
          <tr>
            {data.length > 0 && Object.keys(data[1]).map((key) => (
              <th className='text-capitalize text-center text-white bg-dark' key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {displayedData.map((item, index) => (
            <tr key={index}>
              {Object.values(item).map((val, i) => (
                <td key={i}> { isObject(val) ? <Button onClick={() => { setModalData({ title:  Object.keys(data[1])[i] , description: JSON.stringify(val) }); setShowModal(true); }}>Ver</Button> : val }</td>
              ))}
            </tr>
          ))}
        </tbody>
      </Table>
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
