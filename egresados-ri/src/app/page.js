import './globals.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/headerComponent';
import Footer from './components/footerComponent';
import MetabaseComponent from './components/metabaseComponent';
import SearcherComponent from './components/searcherComponent';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function Home() {
  return (
    <div className="App d-flex flex-column min-vh-100">
    <Router>
        <Header />
        <div className="flex-grow-1">
        <Routes>
            <Route path="/" element={<SearcherComponent />} />
            <Route path="/metabase" element={<MetabaseComponent />} />
          </Routes>
        </div>
        <Footer />
    </Router>
    </div>
  );
}

export default Home;