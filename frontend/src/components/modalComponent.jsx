import React from 'react';
import { Modal, Button } from 'react-bootstrap';
import { JsonView, allExpanded, defaultStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';

const ModalComponent = ({ title, description, show, setShowModal }) => {

    const handleClose = () => setShowModal(false);

    const isJSON = (str) => {
        try {
            JSON.parse(str);
        } catch (e) {
            return false;
        }
        return true;
    };

    console.log(description, isJSON(description));
    if (isJSON(description)) console.log(JSON.parse(description));

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>{title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {isJSON(description) ? (
                    <JsonView data={JSON.parse(description)} shouldExpandNode={allExpanded} style={defaultStyles} />
                ) : (
                    description
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
