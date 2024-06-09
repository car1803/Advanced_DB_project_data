import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/headerComponent';
import Footer from './components/footerComponent';
import MetabaseComponent from './components/metabaseComponent';
import SearcherComponent from './components/searcherComponent';
import DataTableComponent from './components/dataTableComponent';
import ModalComponent from './components/modalComponent';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className="App d-flex flex-column min-vh-100 min-vw-100">
    <Router>
        <Header />
        <div className="flex-grow-1">
          <Routes>
            <Route path="/" element={<SearcherComponent ModalComponent = { ModalComponent } DataTableComponent = { DataTableComponent } />} />
            <Route path="/metabase" element={<MetabaseComponent src={"http://localhost:3300/public/dashboard/df605c0e-186f-4b34-828f-7d350fe6e801"} onlyIframe={false} />} />
          </Routes>
        </div>
        <Footer />
    </Router>
    </div>
  );
}

export default App;
