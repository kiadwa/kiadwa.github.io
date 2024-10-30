import { useEffect, useRef, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

function TrainerChangeInfo() {
    const navigate = useNavigate();
    const { tid, session_token } = useParams();

    const [email, setEmail] = useState('');
    const [f_name, setF_name] = useState('');
    const [l_name, setL_name] = useState('');
    const [password, setPassword] = useState('');
    const [conf_password, setConf_password] = useState('');
    const [trainer, setTrainer] = useState({});
    const [avatar_url_get, setAvatar_url_get] = useState('');
    const [avatar_url, setAvatar_url] = useState('');
    const get_trainer_ep = `${import.meta.env.VITE_TRAINER}`;
    const get_avatar_ep = `${import.meta.env.VITE_TRAINER_AVATAR}`;
    const upload_file_ep = `${import.meta.env.VITE_UPLOAD}`;
    const hasTrainerAvatar = useRef(false);
    const hasTrainerUpload = useRef(false);

    async function fetch_curr_uinfo() {
        try {
            const response = await axios.get(`${get_trainer_ep}?tid=${tid}`, {
                headers: {
                    "token": session_token
                }
            });
            setTrainer(response.data.data.trainer_list[0]);
        } catch (error) {
            console.error("Error fetching trainer info:", error);
            alert("Error fetching trainer info");
        }
    }

    useEffect(() => {
        let isMounted = true;
        async function fetch_curr_uinfo() {
            try {
                const response = await axios.get(`${get_trainer_ep}?tid=${tid}`, {
                    headers: {
                        "token": session_token
                    }
                });
                if (isMounted) {
                    setTrainer(response.data.data.trainer_list[0]);
                }
            } catch (error) {
                if (isMounted) {
                    console.error("Error fetching trainer info:", error);
                    alert("Error fetching trainer info");
                }
            }
        }
        fetch_curr_uinfo();

        return () => {
            isMounted = false;
        };
    }, [tid, session_token]);
    
    async function get_trainer_avatar_url() {
        try {
            const response = await axios.get(`${get_avatar_ep}?tid=${tid}`, {
                headers: {
                    'token': session_token
                }
            });
            setAvatar_url_get(response.data.data.trainer_avatar_list[0]?.avatar || "");
            console.log(avatar_url_get);
        } catch (error) {
            console.error('Error fetching trainer avatar:', error);
        }
    }

    useEffect(() => {
        if (!hasTrainerAvatar.current) {
            get_trainer_avatar_url();
            hasTrainerAvatar.current = true;
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (password !== conf_password) {
            alert("Password mismatch");
            return;
        }
        if (!l_name && !f_name && !email) {
            return;
        }
        let dataToSend = "";
        if (password) {
            dataToSend = {
                data: {
                    "trainer": {
                        "email": trainer.email
                    },
                    "trainer_new": {
                        "l_name": l_name,
                        "f_name": f_name,
                        "email": email,
                        "password": password,
                    }
                }
            };
        } else {
            dataToSend = {
                data: {
                    "trainer": {
                        "email": trainer.email
                    },
                    "trainer_new": {
                        "l_name": l_name,
                        "f_name": f_name,
                        "email": email,
                    }
                }
            };
        }
        
        try {
            await axios.put(get_trainer_ep, dataToSend, {
                headers: {
                    'token': session_token,
                },
                withCredentials: true, 
            });
            alert('Trainer update successful!');
            fetch_curr_uinfo();
        } catch (error) {
            console.error('Error during update information:', error);
            alert('Error during update information');
        }
    }

    const handleCancel = () => {
        navigate(`/thome/${trainer.email}/${session_token}`);
    }

    // handle when trainer upload a pic file
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
                hasTrainerUpload.current = true;
            } catch (error) {
                alert("Error uploading files");
                console.error(error);
            }
        }
    }
    
    async function handleSetAvatar() {
        if (!avatar_url) {
            console.error('No avatar URL to set.');
            return;
        }
    
        if (!avatar_url_get) {
            try {
                const dataToSend = {
                    data: {
                        "trainer_avatar": {
                            "avatar": avatar_url
                        }
                    }
                };
                const response = await axios.post(get_avatar_ep, dataToSend, {
                    headers: {
                        'token': session_token
                    }
                });
                console.log(response)
                console.log('Avatar successfully set.');
                setAvatar_url_get(avatar_url); 
            } catch (error) {
                console.error('Error setting new avatar:', error);
            }
        } else {
            try {
                const dataToSend = {
                    data: {
                        "trainer_avatar": {
                            "tid": tid
                        },
                        "trainer_avatar_new": {
                            "avatar": avatar_url
                        }
                    }
                };
                const response = await axios.put(get_avatar_ep, dataToSend, {
                    headers: {
                        'token': session_token
                    }
                });
                console.log(response)
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
            <p className="h1 text-center mb-5">Update Trainer Information</p>
            <Container style={{ minHeight: '100vh' }}>
                <form onSubmit={handleSubmit}>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">First Name
                                <input type="text" className="form-control" value={f_name} onChange={(e) => setF_name(e.target.value)} />
                                current: {trainer.f_name}
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Last Name
                                <input type="text" className="form-control" value={l_name} onChange={(e) => setL_name(e.target.value)} />
                                current: {trainer.l_name}
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Email
                                <input type="email" className="form-control" value={email} onChange={(e) => setEmail(e.target.value)} />
                                current: {trainer.email}
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
                    <button type="submit" className="btn btn-primary me-2">Update</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
                <form>
                    <label className="form-label">Upload Avatar
                        <input type="file" className="form-control" accept="image/*" onChange={(e) => handleUploadFile(e.target.files[0])} />
                    </label>
                </form>
            </Container>
        </div>
    );
}

export default TrainerChangeInfo;
