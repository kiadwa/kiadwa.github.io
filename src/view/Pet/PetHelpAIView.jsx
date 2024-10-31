import { Container, Form, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "./PetHelpAIView.css";

function PetHelpAIView() {
    const navigate = useNavigate();
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [pet, setPet] = useState({});
    const [user, setUser] = useState({});
    const {pid, uid, session_token} = useParams();
    const get_pet_ep = `${import.meta.env.VITE_PET}`;
    const AI_API_ep = `${import.meta.env.VITE_PETHELP}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`;

    async function fetch_curr_uinfo(){
        
        try{
            const response = await axios.get(`${get_user_ep}?uid=${uid}`,{
                headers: {
                    "token": session_token
                }
            });
            console.log(response.data.data.user_list[0])
            setUser(response.data.data.user_list[0]);
        }catch(error){
            alert("Oops! there is an error in getting your information")
        }
    }

    useEffect(() => {
        let isMounted = true;
        async function fetch_curr_pet_info() {
            try {
                const response = await axios.get(`${get_pet_ep}?pid=${pid}`, {
                    headers: {
                        "token": session_token
                    }
                });
                if (isMounted) {
                    console.log(response.data.data.pet_list[0]);
                    setPet(response.data.data.pet_list[0]);
                }
            } catch (error) {
                if (isMounted) {
                    console.error("Error fetching pet info:", error);
                    alert("Error fetching pet info");
                }
            }
        }
        fetch_curr_pet_info();
        fetch_curr_uinfo();

        return () => {
            isMounted = false;
        };
    }, [uid, session_token]);


    const handleSendMessage = async () => {
        if (input.trim() !== "") {
            // Add user message to chat
            setMessages([...messages, { sender: "user", text: input }]);
            setInput(""); // Clear input field
            const dataToSend = {
                        data:{
                            "pet_help":{
                                "message":input,
                                "diagnosis": pet.diagnosis,
                                "species": pet.species,
                                "breed": pet.breed,
                            }
                        }
            }
            console.log(dataToSend)
            try {
                const response = await axios.post(AI_API_ep, dataToSend, {
                    headers:{
                        
                        'token':session_token
                    }
                } );
                console.log(response.data.data.data);
                // Add bot response to chat
                setMessages(prevMessages => [
                    ...prevMessages,
                    { sender: "bot", text: response.data.data.data }
                ]);
            } catch (error) {
                console.error("Error:", error.response ? error.response.data.error : error.message);
            }
        }
    };
    function handleCancel() {
        const uemail = user.email
        navigate(`/phome/${uemail}/${session_token}`);
    }
    return (
        <div>
        <Container>
            <p className="h1 text-center mb-5">Pet Help AI 💻🐕</p>
            <div className="chat-box">
                <div className="messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={`message ${msg.sender}`}>
                            <span>{msg.text}</span>
                        </div>
                    ))}
                </div>
                <Form className="chat-input" onSubmit={(e) => e.preventDefault()}>
                    <Form.Control
                        type="text"
                        placeholder="Type a message..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                    />
                    <Button onClick={handleSendMessage}>Send</Button>
                </Form>
            </div>
            <button className="btn btn-danger" onClick={handleCancel}>Back</button>
        </Container>
        </div>
    );
}

export default PetHelpAIView;
