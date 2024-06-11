import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import { JsonView, allExpanded, defaultStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

const ModalComponent = ({ title, description, show, searchTerm, setShowModal }) => {

    const handleClose = () => setShowModal(false);

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
      
        return  texto;
    }

    const isJSON = (str) => {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {isJSON(description) ? ( 
                    <div id="span-div-json" load={ 
                        setTimeout(() =>
                        {
                            let divspan = document.getElementById('span-div-json');
                            if(!divspan?.innerHTML) return;
                            divspan.innerHTML = spamConNegrillaEnPalabras(divspan.innerHTML, searchTerm ? searchTerm.split(' ') : []);
                        }, 
                        200) 
                     }>
                        <JsonView data={JSON.parse(description)} shouldExpandNode={allExpanded} style={defaultStyles} />
                    </div>
                ) : (
                    <span dangerouslySetInnerHTML={{ __html: spamConNegrillaEnPalabras(description, searchTerm ? searchTerm.split(' ') : []) }} />
                )}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="primary" onClick={handleClose}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ModalComponent;
