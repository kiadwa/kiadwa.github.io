import { useEffect, useRef, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function RegisterPetOwner() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [f_name, setF_name] = useState('');
    const [l_name, setL_name] = useState('');
    const [password, setPassword] = useState('');
    const [dob, setDoB] = useState('');
    const [description, setDescription] = useState('');
    const [conf_password, setConf_password] = useState('');

    const [csrf_token, setCsrf_token] = useState('');
    const csrf_endpoint = `${import.meta.env.VITE_GET_CSRF_TOKEN}`;
    const register_endpoint = `${import.meta.env.VITE_USER}`;
    const hasFetchedCsrfToken = useRef(false);
    //const cookie_endpoint = `${import.meta.env. VITE_SET_CSRF_COOKIE}`;
    // Helper function to extract cookie value by name
    
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
        
        let currTime = new Date().toISOString().split("T")[1]
        let timestamp = `${dob}T${currTime}`;
        let date = new Date(timestamp);
        let time = date.getTime() / 1000;
        const dataToSend = {
            data:{
                "user": {
                    "email": email,
                    "l_name": l_name,
                    "f_name": f_name,
                    "password": password,
                    "dob": time,
                    "description": description,
                }
            }
        };
        console.log(dataToSend);
        console.log("Csrf token is:", csrf_token)
        try {
            await axios.post(register_endpoint, dataToSend, {
                headers: {
                    'X-CSRFToken': csrf_token, 
                    'token':"<empty>",
                },
                withCredentials: true, 
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
                                <label className="form-label">First Name 
                                <input type="text" className="form-control" id="petowner_fname" value={f_name} onChange={(e) => setF_name(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Last Name
                                <input type="text" className="form-control" id="petowner_lname" value={l_name} onChange={(e) => setL_name(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Email
                                <input type="email" className="form-control" id="petowner_email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">DOB
                                <input type="date" className="form-control" id="petowner_dob" value={dob} onChange={(e) => setDoB(e.target.value)} required/>
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
                        <div className="mb-3">
                            <label className="form-label">Description
                            <input type="text" className="form-control" id="petowner_desc" value={description} onChange={(e) => setDescription(e.target.value)} />
                            </label>
                        </div>
                    </Row>
                    <button type="submit" className="btn btn-primary me-2">Sign Up</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
            </Container>
        </div>
    );
}

export default RegisterPetOwner;
