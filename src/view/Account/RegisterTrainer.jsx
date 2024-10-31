import { Container, Row, Col } from 'react-bootstrap';
import { useState,useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function RegisterTrainer(){
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [f_name, setF_name] = useState('');
    const [l_name, setL_name] = useState('');
    const [password, setPassword] = useState('');
    const [dob, setDoB] = useState('');
    const [conf_password, setConf_password] = useState('');
    const [provid, setProvid] = useState();
    const [providerlist, setProviderlist] = useState([]);

    const [csrf_token, setCsrf_token] = useState('');
    const csrf_endpoint = `${import.meta.env.VITE_GET_CSRF_TOKEN}`;
    const register_endpoint = `${import.meta.env.VITE_TRAINER}`;
    const provider_fetch_endpoint = `${import.meta.env.VITE_PROVIDER}`
    const hasFetchedCsrfToken = useRef(false);


    async function get_provider_list(){
        try{
            const response = await axios.get(provider_fetch_endpoint , {
                headers: {
                    'X-CSRFToken': csrf_token,
                    'token' : '<empty>'
                }
            });
            console.log(response.data.data.provider_list)
            setProviderlist(response.data.data.provider_list);
        }catch (error){
            console.error('Error in fetching provider data', error);
        }
    }


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
    };

    //fetch csrf token and provider list hook
    useEffect(() => {
        if (!hasFetchedCsrfToken.current) {
            get_csrf_token();
            hasFetchedCsrfToken.current = true;
        }
        get_provider_list();
    }, []);

    const handleSubmit = async(e) => {
        e.preventDefault();
        if (password !== conf_password){
            alert("Password mismatch");
            return;
        }
        let currTime = new Date().toISOString().split("T")[1]
        let timestamp = `${dob}T${currTime}`;
        let date = new Date(timestamp);
        let time = date.getTime() / 1000;
        const dataToSend = {
            data:{
                'trainer':{
                    'provid': Number(provid),
                    'email': email,
                    'l_name': l_name,
                    'f_name': f_name,
                    'password': password,
                    'dob': time,
                    }
            }
        }
        console.log(dataToSend);
        console.log("Csrf token is:", csrf_token)
        //request logic to be applied
        try {
            // Make the request to submit the form data with the CSRF token in the headers
            await axios.post(register_endpoint, dataToSend, {
                headers: {
                    'X-CSRFToken': csrf_token,
                    'token' : '<empty>'
                },
                withCredentials: true, // Include credentials for cookies
            });
            alert('Registration successful!');
            handleCancel();
        } catch (error) {
            console.error('Error during registration:', error.data);
            alert('Registration failed. Please try again.');
        }
    }
    
    const handleCancel = () =>{
        navigate('/');
    }
    return(
        <div >
            <p className="h1 text-center mb-5">Sign Up</p>
            <Container style={{ minHeight: '100vh' }}>
            <form>
            <Row>
                <Col>
                <div className="mb-3">
                    <label className="form-label">First Name
                    <input type="text" className="form-control" id="trainer_fname" value={f_name} onChange={(e) => setF_name(e.target.value)} required/>
                    </label>
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Last Name
                    <input type="text" className="form-control" id="trainer_lname" value={l_name} onChange={(e) => setL_name(e.target.value)} required/>
                    </label>
                </div>
                </Col>
                </Row>
                <Row>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Email
                    <input type="email" className="form-control" id="trainer_email" value={email} onChange={(e) => setEmail(e.target.value)} required/>
                    </label>  
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">DOB
                    <input type="date" className="form-control" id="trainer_dob" value={dob} onChange={(e) => setDoB(e.target.value)} required/>
                    </label>
                </div>
                </Col>
                </Row>
                <Row>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Password
                    <input type="password" className="form-control" id="trainer_password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
                    </label>
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Confirm Password
                    <input type="password" className="form-control" id="trainer_confpassword" value={conf_password} onChange={(e) => setConf_password(e.target.value)}/>
                    </label>
                </div>
                </Col>
                <div className="mb-3">
                    <label className="form-label">Provider</label>
                    <select className="form-select" aria-label="Default select example" value={provid} onChange={(e) => setProvid(e.target.value)} required>
                            <option defaultValue={''}>Select your provider</option>
                            {providerlist.map((p) => (
                                <option key={p.provid} value={p.provid}>{p.provider_name}</option>
                                ))
                            };
                            </select>
                </div>
                </Row>
                <button type="submit" className="btn btn-primary me-2" onClick={handleSubmit}>Sign Up</button>
                <button type="cancel" className="btn btn-primary me-2" onClick={handleCancel}>Cancel</button>
            </form>
            </Container>
        </div>
    );
}
export default RegisterTrainer;