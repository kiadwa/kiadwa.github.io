import { useEffect, useState, useRef } from "react";
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
function LogIn(){
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [csrf_token, setCsrf_token] = useState('');
    const [session_token, setSession_token] = useState('');

    const navigate = useNavigate('');
    const {user_type} = useParams();
    const csrf_endpoint = `${import.meta.env.VITE_GET_CSRF_TOKEN}`;
    const login_endpoint = `${import.meta.env.VITE_API}`;
    const hasFetchedCsrfToken = useRef(false);

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
    //fetch csrf token
    useEffect(() => {
        if (!hasFetchedCsrfToken.current) {
            get_csrf_token();
            hasFetchedCsrfToken.current = true;
        }
    }, []);
    //handle submit form
    const handleSubmit = async(e) =>{
        e.preventDefault();
        //handle submit user info into a form and send request to endpoint here
        var dataToSend = undefined

        if (user_type === "user"){
            dataToSend = {
                function: 'user_login',
                data:{
                    "user":{
                        "email": email,
                        "password": password,
                        }
                    }
            }
        }else if (user_type === "trainer"){
            dataToSend = {
                function: 'trainer_login',
                data:{
                    "trainer" : {
                        "email": email,
                        "password": password,
                        }
                    }
            }
        }else{
            dataToSend = {
                function:'provider_login',
                data:{
                    "provider" : {
                        "email": email,
                        "password": password,
                        }
                    }
            }
        }
        try {
            // Make the request to submit the form data with the CSRF token in the headers
            const response = await axios.post(login_endpoint, dataToSend, {
                headers: {
                    'X-CSRFToken': csrf_token, 
                    'token' : '<empty>'
                },
                withCredentials: true,
            });
            console.log(response.data.data.token);
            console.log(session_token)
            handleSuccessLogin(response.data.data.token);
        } catch (error) {
            console.error('Error during log in:', error);
            alert('Log in failed. Please try again.');
        }
    };

    const handleCancel = () =>{
        navigate('/');
    };

    function handleSuccessLogin(ss_token){
        if (user_type === "user"){
           navigate(`/phome/${email}/${ss_token}`)
        }else if (user_type === "trainer"){
            navigate(`/thome/${email}/${ss_token}`)
        }else{
            navigate(`/provhome/${email}/${ss_token}`)
        }
    }

    return(
        <div >
            <p className="h1 text-center mb-5">Sign In</p>
            <Container style={{ minHeight: '100vh' }}>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Email address</label>
                    <input type="email" 
                    className="form-control" 
                    id="exampleInputEmail1" 
                    aria-describedby="emailHelp" 
                    value={email} onChange={(e) => {setEmail(e.target.value)}}/>
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input type="password" 
                    className="form-control" 
                    id="exampleInputPassword1" 
                    value={password}
                    onChange={(e) => {setPassword(e.target.value)}}/>
                </div>
                
                <button type="submit" className="btn btn-primary me-2" onClick={handleSubmit}>Log In</button>
                <button type="cancel" className="btn btn-danger me-2" onClick={handleCancel}>Cancel</button>
            </form>
            </Container>
        </div>
    );
}
export default LogIn;