import axios from "axios";
import { useEffect, useState } from "react";
import { Container, Row, Card, Col, CardTitle, CardText } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";

function ProviderHome(){
    const [myorderlist, setMyOrderList] = useState([]);
    const [myProvider, setMyProvider] = useState([]);
    const [trainer, setTrainer] = useState([]);
    const [provider, setProvider] = useState({});

    const { email, session_token } = useParams();
    const navigate = useNavigate();

    const get_order_ep = `${import.meta.env.VITE_SERVICE}`;
    const get_trainer_ep = `${import.meta.env.VITE_TRAINER}`;
    const get_provider_ep = `${import.meta.env.VITE_PROVIDER}`;

    useEffect(() => {
        let isMounted = true;

        async function fetchData() {
            try {
                // Step 1: Fetch current trainer info
                const providerResponse = await axios.get(`${get_provider_ep}?email=${email}`, {
                    headers: {
                        "token": session_token,
                    },
                });
                if (isMounted) {
                    const providerData = providerResponse.data.data.provider_list[0];
                    setProvider(providerData);

                    const orderResponse = await axios.get(`${get_trainer_ep}?tid=${providerData.provid}`, {
                        headers: {
                            "token": session_token,
                        },
                    });
                    if (isMounted) {
                        setTrainer(orderResponse.data.data.trainer_list);
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

    function handleLogOut(){
        navigate('/');
    }

    return (
        <div className="container-fluid">
            <Container>
            <p className="h1 text-center mb-5">🐱🐶PetXercise🐹🐰</p>
                <Row>
                    <h1>About Me</h1>
                    <Card>
                        <CardTitle>
                            {provider.name}
                        </CardTitle>
                        <CardText>
                            📧{provider.email}
                        </CardText>
                        <CardText>
                            📞{provider.phone_number}
                        </CardText>
                    </Card>
                </Row>
                <Row>
                    <h1>My Trainer</h1>
                    {trainer.map((t) => (
                    <Card className="m-2  w-25 h-25" key={t.tid}>
                        
                        <CardTitle>{t.l_name + " " + t.f_name}</CardTitle>
                        <CardText>📧{t.email}</CardText>  
                    </Card>
                ))
                }
                </Row>
                <button className="btn btn-danger" onClick={handleLogOut}>Log out</button>
            </Container>
        </div>
        );
}
export default ProviderHome;