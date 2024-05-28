import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/headerComponent';
import Footer from './components/footerComponent';
import MetabaseComponent from './components/metabaseComponent';
import SearcherComponent from './components/searcherComponent';
import { Container, Row } from 'react-bootstrap';

function App() {
  return (
    <div className="App d-flex flex-column min-vh-100">
      <Header />
      <div className="flex-grow-1">
        <Container className="text-start">
          <Row>
            <SearcherComponent />
          </Row>
          <Row>
            <MetabaseComponent />
          </Row>
        </Container>
      </div>
      <Footer />
    </div>
  );
}

export default App;
