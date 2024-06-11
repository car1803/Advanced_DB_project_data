import React from 'react';
import { Container, Row } from 'react-bootstrap';

const MetabaseComponent = ({ src, onlyIframe }) => {

    if (!src) {
        return null;
    }

    if (onlyIframe) {
        return (
            <iframe
                    src={src}
                    title="Metabase Dashboard"
                    width="100%"
                    height="800"
                    allowFullScreen
            ></iframe>
        )
    }

    return (
        <Container>
            <h2 className='m-4'>Información resumida:</h2>
            <Row>
                <iframe
                    src={src}
                    title="Metabase Dashboard"
                    width="100%"
                    height="800"
                    allowFullScreen
                ></iframe>
            </Row>
        </Container>
    );
};

export default MetabaseComponent;
