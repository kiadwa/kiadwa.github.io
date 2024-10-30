import { useEffect, useRef, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function ProviderRegister() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [provider_name, setProvider_name] = useState('');
    const [password, setPassword] = useState('');
    const [conf_password, setConf_password] = useState('');
    const [phone_number, setPhone_number] = useState('');
    const [csrf_token, setCsrf_token] = useState('');
    const csrf_endpoint = `${import.meta.env.VITE_GET_CSRF_TOKEN}`;
    const register_endpoint = `${import.meta.env.VITE_PROVIDER}`;
    const hasFetchedCsrfToken = useRef(false);
    //const cookie_endpoint = `${import.meta.env. VITE_SET_CSRF_COOKIE}`;
    // Helper function to extract cookie value by name
    {/*
    :param data: 	{
        "provider": {
            "provider_name": "str",
            "email": "str",
            "phone_number": "str",
            "password": "str",
            "verification": false
        }
    }
    :return: 	{
        "error_code": 200,
        "data": null,
        "error_msg": "str?"
    }
        */}
    async function get_csrf_token() {
        try {
            const response = await axios.get(csrf_endpoint, {
                withCredentials: true
            });
            console.log(response.data.csrftoken)
            setCsrf_token(response.data.csrftoken)
        } catch (error) {
            console.error('Error fetching CSRF token:', error);
        }
    }
    useEffect(() => {
        if (!hasFetchedCsrfToken.current) {
            get_csrf_token();
            hasFetchedCsrfToken.current = true;
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== conf_password) {
            alert("Password mismatch");
            return;
        }
        
        const dataToSend = {
            data:{
                "provider": {
                    "email": email,
                    "provider_name": provider_name,
                    "password": password,
                    "phone_number": phone_number,
                }
            }
        };
        console.log(dataToSend);
        console.log("Csrf token is:", csrf_token)
        try {
            // Make the request to submit the form data with the CSRF token in the headers
            await axios.post(register_endpoint, dataToSend, {
                headers: {
                    'X-CSRFToken': csrf_token, 
                    'token':"<empty>",
                },
                withCredentials: true, // Include credentials for cookies
            });
            alert('Registration successful!');
            handleCancel();
        } catch (error) {
            console.error('Error during registration:', error);
            alert('Registration failed. Please try again.');
        }
    }

    const handleCancel = () => {
        navigate('/');
    }

    return (
        <div>
            <p className="h1 text-center mb-5">Sign Up</p>
            <Container style={{ minHeight: '100vh' }}>
                <form onSubmit={handleSubmit}>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Provider Name
                                <input type="text" className="form-control" id="p_name" value={provider_name} onChange={(e) => setProvider_name(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Email
                                <input type="email" className="form-control" id="provider_email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Phone number
                                <input type="text" className="form-control" id="provide_phone_number" value={phone_number} onChange={(e) => setPhone_number(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Password
                                <input type="password" className="form-control" id="petowner_password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Confirm Password
                                <input type="password" className="form-control" id="petowner_confpassword" value={conf_password} onChange={(e) => setConf_password(e.target.value)} />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <button type="submit" className="btn btn-primary me-2">Sign Up</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
            </Container>
        </div>
    );
}

export default ProviderRegister;
