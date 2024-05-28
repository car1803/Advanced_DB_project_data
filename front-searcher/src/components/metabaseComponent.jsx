import React from 'react';
import { Container, Row } from 'react-bootstrap';
import { useEffect } from 'react';

const MetabaseComponent = () => {
    useEffect(() => {
        console.log('MetabaseComponent mounted');
    }, []);
    
    return (
        <Container>
            <h2 className='m-4'>Información resumida:</h2>
            <Row>
                <iframe
                    src="http://localhost:3300/public/dashboard/df605c0e-186f-4b34-828f-7d350fe6e801"
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