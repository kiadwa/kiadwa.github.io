import { useState, useRef, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function ServiceView() {
    const navigate = useNavigate();
    const { oid, uid, session_token } = useParams();
    const [service, setService] = useState({});
    const [trainer, setTrainer] = useState({});
    const [uemail, setUemail] = useState('');
    const isPaid = useRef(false);
    const [isPaidState, setIsPaidState] = useState(false); // State to trigger re-render
    const get_service_ep = `${import.meta.env.VITE_SERVICE}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`;
    const get_trainer_ep = `${import.meta.env.VITE_TRAINER}`;
    const get_payment_ep = `${import.meta.env.VITE_PAYMENT}`;

    // Fetch all necessary data in a sequence
    useEffect(() => {
        let isMounted = true;

        async function fetchData() {
            try {
                //fetch payment list
                const paymentResponse = await axios.get(`${get_payment_ep}?order_id=${oid}`, {
                    headers: {
                        'token': session_token
                    }
                });
                const payment_list = paymentResponse.data.data.payment_list;
                if (isMounted && payment_list.length > 0) {
                    isPaid.current = true;
                    setIsPaidState(true); // Update state to reflect the value of isPaid.current
                }

                // fetch user info
                const userResponse = await axios.get(`${get_user_ep}?uid=${uid}`, {
                    headers: {
                        "token": session_token
                    }
                });
                if (isMounted) {
                    setUemail(userResponse.data.data.user_list[0].email);
                }

                // fetch service info
                const serviceResponse = await axios.get(`${get_service_ep}?order_id=${oid}`, {
                    headers: {
                        'token': session_token
                    }
                });
                if (isMounted) {
                    setService(serviceResponse.data.data.service_order_list[0]);
                }

                // fetch trainer info (dependent on service info)
                const tid = Number(serviceResponse.data.data.service_order_list[0].tid);
                const trainerResponse = await axios.get(`${get_trainer_ep}?tid=${tid}`, {
                    headers: {
                        'token': session_token
                    }
                });
                if (isMounted) {
                    setTrainer(trainerResponse.data.data.trainer_list[0]);
                }
            } catch (error) {
                if (isMounted) {
                    console.error("Error fetching data:", error);
                    alert("An error occurred while fetching data.");
                }
            }
        }

        fetchData();

        return () => {
            isMounted = false;
        };
    }, [oid, uid, session_token]);

    // Handle navigation to payment page
    function handlePetHelpAI() {
        navigate(`/payment/${oid}/${uid}/${trainer.tid}/${session_token}`);
    }

    // Handle cancel action
    function handleCancel() {
        navigate(`/phome/${uemail}/${session_token}`);
    }

    return (
        <div>
            <Container>
                <p className="h1 text-center mb-5">My Order ⚒</p>
                <form>
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Service ID
                                    <input type="text" className="form-control" id="p_name" defaultValue={service.order_id || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Trainer first name
                                    <input type="text" className="form-control" id="tf_name" defaultValue={trainer.l_name || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Trainer last name
                                    <input type="text" className="form-control" id="tl_name" defaultValue={trainer.f_name || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Trainer email
                                    <input type="text" className="form-control w-100" id="service" defaultValue={trainer.email || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Cost ($AUD)
                                    <input type="text" className="form-control w-100" id="cost" defaultValue={service.cost || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Service type
                                    <input type="text" className="form-control w-100" id="service_type" defaultValue={service.service_type || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                        <Col>
                            <div className="mb-10">
                                <label className="form-label">Status
                                    <input type="text" className="form-control w-100" id="status" defaultValue={service.status || ''} readOnly />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <button type="button" className="btn btn-success me-2" disabled={isPaidState} onClick={handlePetHelpAI}>Pay</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
            </Container>
        </div>
    );
}

export default ServiceView;
