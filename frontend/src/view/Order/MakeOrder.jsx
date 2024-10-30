import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { Container, Row, Col } from "react-bootstrap";

function MakeOrder() {
    const navigate = useNavigate();
    const { uid, tid, session_token } = useParams();
    const [pet_list, setPet_list] = useState([]);
    const [cost, setCost] = useState('');
    const [uemail, setUemail] = useState('');
    const [pet_id, setPet_id] = useState('');
    const [service, setService] = useState('');
    const [order_id, setOrder_id] = useState();
    const [trainerobj, setTrainerobj] = useState({});
    const make_order_ep = `${import.meta.env.VITE_SERVICE}`;
    const fetch_my_pet_ep = `${import.meta.env.VITE_PET}`;
    const fetch_trainer_info_ep = `${import.meta.env.VITE_TRAINER}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`;

    // Fetch user information
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
                    console.log(response.data.data.user_list[0].email);
                    setUemail(response.data.data.user_list[0].email);
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

    // Fetch trainer and pet information
    useEffect(() => {
        if (uid) {
            let isMounted = true;

            async function fetch_trainer_info() {
                try {
                    const response = await axios.get(`${fetch_trainer_info_ep}?tid=${tid}`, {
                        headers: {
                            'token': session_token
                        }
                    });
                    if (isMounted) {
                        setTrainerobj(response.data.data.trainer_list[0]);
                    }
                } catch (error) {
                    if (isMounted) {
                        console.error("Error fetching trainer info:", error);
                    }
                }
            }

            async function fetch_my_pet_list() {
                try {
                    const response = await axios.get(`${fetch_my_pet_ep}?uid=${uid}`, {
                        headers: {
                            'token': session_token
                        }
                    });
                    if (isMounted) {
                        setPet_list(response.data.data.pet_list);
                    }
                } catch (error) {
                    if (isMounted) {
                        console.error("Error fetching pet list:", error);
                    }
                }
            }

            fetch_trainer_info();
            fetch_my_pet_list();

            return () => {
                isMounted = false;
            };
        }
    }, [uid, session_token, tid]);

    // Handle form submission
    async function handleSubmit(event) {
        event.preventDefault(); // Prevent page refresh

        let date = new Date(); // Current date and time
        let time = date.getTime() / 1000; // Convert to Unix timestamp in seconds
        const dataToSend = {
            "data":{
            "service_order": {
                "pid": Number(pet_id),
                "tid": Number(tid),
                "service_type": service,
                "cost": Number(cost),
                "status": "Pending",
                "order_date": time
            }
        }    
        };
        console.log(dataToSend);
        try {
            const response = await axios.post(make_order_ep, dataToSend, {
                headers:{
                    'token': session_token,
                },
                withCredentials: true,
            });
            console.log(response.data.data.order_id);
            setOrder_id(response.data.data.order_id);
            alert("Order created successfully!");
            navigate(`/payment/${response.data.data.order_id}/${uid}/${tid}/${session_token}`)
        } catch (error) {
            console.error("Problem with making order:", error);
            alert("Problem with make order.");
        }
    }

    // Handle cancel action
    function handleCancel() {
        navigate(`/phome/${uemail}/${session_token}`);
    }

    return (
        <div>
            <Container>
                <p className="h1 text-center mb-5">Make Order 🤝</p>
                <form onSubmit={handleSubmit}>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Trainer first name
                                    <input type="text" className="form-control" id="trainer_fname" value={trainerobj?.f_name || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Trainer last name
                                    <input type="text" className="form-control" id="trainer_lname" value={trainerobj?.l_name || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Email
                                    <input type="text" className="form-control" id="trainer_email" value={trainerobj?.email || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Select your pet</label>
                                <select className="form-select" id="pet_id" value={pet_id} onChange={(e) => { setPet_id(e.target.value) }}>
                                    <option value=''>Select your pet for service</option>
                                    {pet_list.map((p) => (
                                        <option key={p.pid} value={p.pid}>{p.p_name}</option>
                                    ))}
                                </select>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Service
                                    <input type="text" className="form-control w-100" id="service" value={service} onChange={(e) => { setService(e.target.value) }} />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Price
                                    <input type="text" className="form-control w-100" id="price" value={cost} onChange={(e) => { setCost(e.target.value) }} />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <button type="submit" className="btn btn-primary me-2">Create</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
            </Container>
        </div>
    );
}
export default MakeOrder;