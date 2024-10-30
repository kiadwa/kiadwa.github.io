import { useEffect, useRef, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

function PetOwnerChangeInfo() {
    const navigate = useNavigate();
    const { uid, session_token } = useParams();

    const [email, setEmail] = useState('');
    const [f_name, setF_name] = useState('');
    const [l_name, setL_name] = useState('');
    const [password, setPassword] = useState('');
    const [description, setDescription] = useState('');
    const [conf_password, setConf_password] = useState('');
    const [user, setUser] = useState({});
    const [avatar_url_get, setAvatar_url_get] = useState('');
    const [avatar_url, setAvatar_url] = useState('');
    const register_endpoint = `${import.meta.env.VITE_USER}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`;
    const get_avatar_ep = `${import.meta.env.VITE_USER_AVATAR}`;
    const upload_file_ep = `${import.meta.env.VITE_UPLOAD}`;
    const avatar_load_ep = `${import.meta.env.VITE_AVATAR}`;
    const hasUserAvatar = useRef(false);
    const hasUserUpload = useRef(false);

    async function fetch_curr_uinfo() {
        try {
            const response = await axios.get(`${get_user_ep}?uid=${uid}`, {
                headers: {
                    "token": session_token
                }
            });
            
            setUser(response.data.data.user_list[0]);
        } catch (error) {
            console.error("Error fetching user info:", error);
            alert("Error fetching user info");
        }
    }
    useEffect(() => {
        let isMounted = true;
        async function fetch_curr_uinfo() {
            try {
                const response = await axios.get(`${get_user_ep}?uid=${uid}`, {
                    headers: {
                        "token": session_token
                    }
                });
                if (isMounted) {
                    setUser(response.data.data.user_list[0]);
                }
            } catch (error) {
                if (isMounted) {
                    console.error("Error fetching user info:", error);
                    alert("Error fetching user info");
                }
            }
        }
        fetch_curr_uinfo();

        return () => {
            isMounted = false;
        };
    }, [uid, session_token]);
    //fetch existing avatar if exist
    async function get_user_avatar_url() {
        try {
            const response = await axios.get(`${get_avatar_ep}?uid=${uid}`, {
                headers:{
                    'token':session_token
                }
            });
            console.log(response.data.data.user_avatar_list)
            setAvatar_url_get(response.data.data.user_avatar_list[0].avatar)
        } catch (error) {
            console.error('Error fetching user avatar:', error);
        }
    }
    useEffect(() => {
        if (!hasUserAvatar.current) {
            get_user_avatar_url();
            hasUserAvatar.current = true;
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== conf_password) {
            alert("Password mismatch");
            return;
        }
        if(!l_name && !f_name && !email && !description){
            return;
        }
        var dataToSend=""
        if(password){
            dataToSend = {
                data:{
                    "user":{
                      "email": user.email
                    },
                    "user_new": {
                        "l_name": l_name,
                        "f_name": f_name,
                        "email": email,
                        "password": password,
                        "description": description,
                    }
                }
            }
        }else{
            dataToSend = {
                data:{
                    "user":{
                      "email": user.email
                    },
                    "user_new": {
                        "l_name": l_name,
                        "f_name": f_name,
                        "email": email,
                        "description": description,
                    }
                }
            }
        }
        
        try {
            // Make the request to submit the form data with the CSRF token in the headers
            await axios.put(register_endpoint, dataToSend, {
                headers: {
                    'token': session_token,
                },
                withCredentials: true, // Include credentials for cookies
            });
            alert('User update successful!');
            fetch_curr_uinfo();
        } catch (error) {
            console.error('Error during update information:', error);
            alert('Error during update information');
        }
    }

    const handleCancel = () => {
        navigate(`/phome/${user.email}/${session_token}`);
    }

    // handle when user upload a pic file
    async function handleUploadFile(file) {
        if (file) {
            const dataToSend = new FormData();
            dataToSend.append('file', file);
            try {
                const response = await axios.post(upload_file_ep, dataToSend, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'token': session_token
                    }
                });
                if (response.data && response.data.data.url) {
                    console.log('File uploaded successfully:', response.data.data.url);
                    setAvatar_url(response.data.data.url); 
                } else {
                    console.error('File upload response does not contain a URL:', response.data);
                }
                hasUserUpload.current = true;
            } catch (error) {
                alert("Error uploading files");
                console.error(error);
            }
        }
    }
    
    //handle when user decide to register that avatar as his
    async function handleSetAvatar() {
        console.log("new a url: " + avatar_url)
        if (!avatar_url) {
            console.error('No avatar URL to set.');
            return;
        }
    
        console.log("existing a url " + avatar_url_get)
        if (!avatar_url_get) {
            try {
                const dataToSend = {
                    data: {
                        "user_avatar": {
                            "avatar": avatar_url
                        }
                    }
                };
                console.log("1 " + JSON.stringify(dataToSend)); 
                await axios.post(get_avatar_ep, dataToSend, {
                    headers: {
                        'token': session_token
                    }
                });
                console.log('Avatar successfully set.');
                setAvatar_url_get(avatar_url); 
            } catch (error) {
                console.error('Error setting new avatar:', error);
            }
        } else {
            try {
                const dataToSend = {
                    data: {
                        "user_avatar": {
                            "uid": uid
                        },
                        "user_avatar_new": {
                            "avatar": avatar_url
                        }
                    }
                };
                console.log("2 " + JSON.stringify(dataToSend));
                await axios.put(get_avatar_ep, dataToSend, {
                    headers: {
                        'token': session_token
                    }
                });
                console.log('Avatar successfully updated.');
                setAvatar_url_get(avatar_url); 
            } catch (error) {
                console.error('Error updating avatar:', error);
            }
        }
    }
    useEffect(() => {
        if (avatar_url) {
            handleSetAvatar();
        }
    }, [avatar_url]);
    return (
        <div>
            <p className="h1 text-center mb-5">Update User Information</p>
            <Container style={{ minHeight: '100vh' }}>
                <form onSubmit={handleSubmit}>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">First Name
                                <input type="text" className="form-control" value={f_name} onChange={(e) => setF_name(e.target.value)} />
                                current: {user.f_name}
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Last Name
                                <input type="text" className="form-control" value={l_name} onChange={(e) => setL_name(e.target.value)} />
                                current: {user.l_name}
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Email
                                <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} />
                                current: {user.email}
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Password
                                <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Confirm Password
                                <input type="password" className="form-control" value={conf_password} onChange={(e) => setConf_password(e.target.value)} />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <div className="mb-3">
                            <label className="form-label">Description
                            <input type="text" className="form-control" value={description} onChange={(e) => setDescription(e.target.value)} />
                            current: {user.description}
                            </label>
                        </div>
                    
                    </Row>
                    <button type="submit" className="btn btn-primary me-2">Update</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
                <form >
                    <label className="form-label">Upload Avatar
                                <input type="file" className="form-control" accept="image/*" onChange={(e) => {handleUploadFile(e.target.files[0])}} />
                                {/*<button type="button" className='btn btn-primary' onClick={handleSetAvatar}>Save avatar</button>*/}
                                </label>
                </form>
            </Container>
        </div>
    );
}

export default PetOwnerChangeInfo;
