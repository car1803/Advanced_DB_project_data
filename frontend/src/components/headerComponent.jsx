import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';

const Header = () => {
  return (
    <Navbar bg="dark" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand href="/">Egresados</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="/">Busqueda</Nav.Link>
            <Nav.Link href="/metabase">Metabase</Nav.Link>
            <Nav.Link href="http://localhost:3300/"><Button className='btn-light' style={{ padding: "2px 5px" }}>Gestionar Metabase</Button></Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
