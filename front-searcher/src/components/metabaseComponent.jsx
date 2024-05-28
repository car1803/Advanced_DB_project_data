import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const MetabaseComponent = () => {
    return (
        <Container>
            <h2 className='m-4'>Información resumida:</h2>
            <Row>
                <Col>
                    <iframe
                         src="http://localhost:3300/public/dashboard/df605c0e-186f-4b34-828f-7d350fe6e801"
                        title="Metabase Dashboard"
                        width="100%"
                        height="600"
                        allowFullScreen
                        allowTransparency
                    ></iframe>
                </Col>
            </Row>
        </Container>
    );
};

export default MetabaseComponent;