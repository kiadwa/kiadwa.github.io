import axios from "axios";
import { useEffect, useState } from "react";
import { Container, Row, Card, Col, CardTitle, CardText, CardImg, CardHeader, CardBody } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

function TrainerHome() {
    const [myorderlist, setMyOrderList] = useState([]);
    const [myProvider, setMyProvider] = useState([]);
    const [trainer, setTrainer] = useState({});
    const [trainer_avatar_url, setTrainer_avatar_url] = useState('');
    const [trainer_avatar, setTrainer_avatar] = useState();
    const { email, session_token } = useParams();
    const navigate = useNavigate();

    const get_order_ep = `${import.meta.env.VITE_SERVICE}`;
    const get_trainer_ep = `${import.meta.env.VITE_TRAINER}`;
    const get_provider_ep = `${import.meta.env.VITE_PROVIDER}`;
    const get_trainer_avatar_ep = `${import.meta.env.VITE_TRAINER_AVATAR}`;
    const avatar_load_ep = `${import.meta.env.VITE_AVATAR}`;

    useEffect(() => {
        let isMounted = true;

        async function fetchData() {
            try {
                const trainerResponse = await axios.get(`${get_trainer_ep}?email=${email}`, {
                    headers: {
                        "token": session_token,
                    },
                });
                if (isMounted) {
                    const trainerData = trainerResponse.data.data.trainer_list[0];
                    setTrainer(trainerData);

                    const orderResponse = await axios.get(`${get_order_ep}?tid=${trainerData.tid}`, {
                        headers: {
                            "token": session_token,
                        },
                    });
                    if (isMounted) {
                        setMyOrderList(orderResponse.data.data.service_order_list);
                    }

                    // Fetch provider list based on provider ID
                    const providerResponse = await axios.get(`${get_provider_ep}?provid=${trainerData.provid}`, {
                        headers: {
                            "token": session_token,
                        },
                    });
                    if (isMounted) {
                        setMyProvider(providerResponse.data.data.provider_list);
                    }
                }
            } catch (error) {
                console.error("Error fetching data:", error);
                alert("Oops! There was an error fetching data.");
            }
        }

        fetchData();

        return () => {
            isMounted = false;
        };
    }, [email, session_token]);

    useEffect(() => {
        if (trainer.tid) { 
            fetch_trainer_avatar();
        }
    }, [trainer, session_token]);

    useEffect(() => {
        if (trainer_avatar_url) { 
            fetch_trainer_avatar_file();
        }
    }, [trainer_avatar_url, session_token]);

    async function fetch_trainer_avatar() {
        try {
            const response = await axios.get(`${get_trainer_avatar_ep}?tid=${trainer.tid}`, {
                headers: {
                    "token": session_token,
                },
            });
            const avatar = response.data.data.trainer_avatar_list[0]?.avatar;
            console.log(response.data.data)
            
            if (avatar) {
                setTrainer_avatar_url(avatar);
            }
        } catch (error) {
            alert("Oops! there is an error in getting your information");
            console.error("Error fetching trainer avatar:", error);
        }
    }

    async function fetch_trainer_avatar_file() {
        try {
            const response = await axios.get(`${avatar_load_ep}/${trainer_avatar_url}`, {
                headers: {
                    "token": session_token,
                },
                responseType: 'arraybuffer', // Get binary data
            });

            const base64 = btoa(
                new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), '')
            );

            setTrainer_avatar(`data:image/jpeg;base64,${base64}`);
        } catch (error) {
            alert("Oops! there is an error in getting your avatar image");
            console.error("Error fetching trainer avatar image:", error);
        }
    }

    function handleLogOut() {
        navigate('/');
    }

    function navigateChangeInfo() {
        navigate(`/trainer-update/${trainer.tid}/${session_token}`);
    }

    return (
        <div className="container-fluid">
            <Container>
                <p className="h1 text-center mb-5">🐱🐶PetXercise🐹🐰</p>
                <Row>
                    <h2 style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
                        Me 🧑
                        <Card
                            className="w-50"
                            style={{
                                border: "1px solid #ddd",
                                borderRadius: "10px",
                                boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                                overflow: "hidden",
                                padding: "1rem",
                                textAlign: "center",
                            }}>
                            <CardImg
                                variant="top"
                                src={trainer_avatar ? trainer_avatar : "https://via.placeholder.com/150"}
                                alt="Trainer Image"
                                style={{ width: "120px", height: "120px", objectFit: "cover", borderRadius: "50%", margin: "0 auto" }}
                            />
                            <CardHeader style={{ backgroundColor: "#f8f9fa", borderBottom: "1px solid #ddd", padding: "0.5rem" }}></CardHeader>
                            <CardBody>
                                <CardText style={{ fontWeight: "bold", fontSize: "1.25rem" }}>{trainer.l_name + " " + trainer.f_name}</CardText>
                                <CardTitle style={{ color: "#555", marginBottom: "0.5rem" }}>✉ {trainer.email}</CardTitle>
                                <button className="btn btn-primary" style={{ alignSelf: "flex-end" }} onClick={navigateChangeInfo}>
                                    Change info
                                </button>
                            </CardBody>
                        </Card>
                    </h2>
                </Row>
                <Row>
                    <h1>My Provider💼</h1>
                    {myProvider.map((prov) => (
                        <Card className="m-2 w-25 h-25" key={prov.provid}>
                            <CardTitle>{prov.provider_name}</CardTitle>
                            <CardText>📧{prov.email}</CardText>
                            <CardText>📞{prov.phone_number}</CardText>
                        </Card>
                    ))}
                </Row>
                <Row>
                    <h1>Current Service🐕‍🦺</h1>
                    {myorderlist.map((order) => (
                        <Card className="m-2 w-25 h-25" key={order.order_id}>
                            <CardTitle>{order.service_type}</CardTitle>
                            <CardText>💲{order.cost}</CardText>
                            <CardText>💨{order.status}</CardText>
                            <button className="btn btn-primary">View</button>
                        </Card>
                    ))}
                </Row>
                <button className="btn btn-danger" onClick={handleLogOut}>Log out</button>
            </Container>
        </div>
    );
}

export default TrainerHome;
