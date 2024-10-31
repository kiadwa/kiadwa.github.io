import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { Container, Row, Card, CardHeader, CardBody, CardTitle, CardText, Col, CardImg } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
{/**
    headers: {
                    'X-CSRFToken': csrf_token, 
                    'token' : '<session token here>'
                }
 */}


function PetOwnerHome(){
    const navigate = useNavigate();
    const [trainerlist, setTrainerlist] = useState([]);
    const [myorderlist, setMyOrderList] = useState([]);
    const [mypetlist, setMyPetList] = useState([]);
    const [uid, setUid] = useState('');
    const [user, setUser] = useState({});
    const [user_avatar_url, setUser_avatar_url] = useState('');
    const [user_avatar, setUser_avatar] = useState({});
    const {email,session_token} = useParams();

    const get_user_ep = `${import.meta.env.VITE_USER}`;
    const get_trainer_ep= `${import.meta.env.VITE_TRAINER}`;
    const get_order_ep= `${import.meta.env.VITE_SERVICE}`;
    const get_pet_ep=`${import.meta.env.VITE_PET}`;
    const get_user_avatar_ep = `${import.meta.env.VITE_USER_AVATAR}`;
    const avatar_load_ep = `${import.meta.env.VITE_AVATAR}`;

    async function fetch_user_avatar(){
        try{
            const response = await axios.get(`${get_user_avatar_ep}?uid=${uid}`,{
                headers: {
                    "token": session_token
                }
            });
            console.log(response.data.data.user_avatar_list[0].avatar)
            setUser_avatar_url(response.data.data.user_avatar_list[0].avatar)
            return response.data.data.user_avatar_list[0].avatar
        }catch(error){
            alert("Oops! there is an error in getting your information")
        }
    }
    async function fetch_user_avatar_file() {
        try {
            const response = await axios.get(`${avatar_load_ep}/${user_avatar_url}`, {
                headers: {
                    "token": session_token
                },
                responseType: 'arraybuffer' 
            });
    
            const base64 = btoa(
                new Uint8Array(response.data)
                    .reduce((data, byte) => data + String.fromCharCode(byte), '')
            );
    
            setUser_avatar(`data:image/jpeg;base64,${base64}`); 
        } catch (error) {
            alert("Oops! there is an error in getting your avatar image");
            console.error("Error fetching user avatar image:", error);
        }
    }
    async function fetch_curr_uinfo(){
        
        try{
            const response = await axios.get(`${get_user_ep}?email=${email}`,{
                headers: {
                    "token": session_token
                }
            });
            setUid(response.data.data.user_list[0].uid);
            setUser(response.data.data.user_list[0])
        }catch(error){
            alert("Oops! there is an error in getting your information")
        }
    }

    async function fetch_trainer_list() {
        
        try{
            const response = await axios.get(get_trainer_ep,{
                headers: {
                    "token": session_token
                }});
            setTrainerlist(response.data.data.trainer_list)
        }catch(error){
            alert("Error fetching all trainer", error);
        }
    }
    async function fetch_my_order_list() {
        try{
            const response = await axios.get(`${get_order_ep}?uid=${uid}`,{
                headers: {
                    "token": session_token
                }
            })
            setMyOrderList(response.data.data.service_order_list);
        }catch(error){
            
        }
    }
    async function fetch_my_pet_list() {
        try{
            const response = await axios.get(`${get_pet_ep}?uid=${uid}`,{
                headers: {
                    "token": session_token
                }
            })
            setMyPetList(response.data.data.pet_list);
        }catch(error){
            
        }
    }
    function navigateBooking(tid){
        navigate(`/order/${tid}/${uid}/${session_token}`)
    }
    function navigatePetView(pid){
        navigate(`/pet/${pid}/${uid}/${session_token}`)
    }
    function navigateAddPet(){
        navigate(`/pet-register/${uid}/${session_token}`)
    }
    function navigateTrainerAbout(){

    }
    function navigateOrderDetail(oid){
        navigate(`/service/${oid}/${uid}/${session_token}`);
    }
    function navigateChangeInfo(){
        navigate(`/user-update/${uid}/${session_token}`)
    }

    useEffect(() => {
        fetch_curr_uinfo();
        fetch_trainer_list();
        fetch_my_order_list();
        fetch_my_pet_list();
        fetch_user_avatar();
        fetch_user_avatar_file();

    },[uid, session_token]);
    
    return(
        <div className="container-fluid">
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
                        }}
                    >
                        <CardImg
                            variant="top"
                            src={user_avatar ? user_avatar : "https://via.placeholder.com/150"}
                            alt="User Image"
                            style={{ width: "120px", height: "120px", objectFit: "cover", borderRadius: "50%", margin: "0 auto" }}
                        />
                        <CardHeader style={{ backgroundColor: "#f8f9fa", borderBottom: "1px solid #ddd", padding: "0.5rem" }}></CardHeader>
                        <CardBody>
                            <CardText style={{ fontWeight: "bold", fontSize: "1.25rem" }}>{user.l_name + " " + user.f_name}</CardText>
                            <CardTitle style={{ color: "#555", marginBottom: "0.5rem" }}>✉ {user.email}</CardTitle>
                            <CardTitle style={{ color: "#777", fontStyle: "italic" }}>🌵 {user.description}</CardTitle>
                            <button className="btn btn-primary" style={{ alignSelf: "flex-end" }} onClick={navigateChangeInfo}>
                                Change info
                            </button>
                        </CardBody>
                    </Card>
            </h2>
            </Row>
            <Row>
                <h2>Trainers 👟
                <button className="btn btn-primary w-2">Refresh</button>
                </h2>
 
                {trainerlist.map((t) => (
                    <Card className="m-2  w-25 h-25" key={t.tid} >
                        <CardTitle>{t.l_name+" "+t.f_name}</CardTitle>
                        <CardText>✉{t.email}</CardText>
                        <Row>
                            <Col>
                            <button className="btn btn-success" onClick={()=>{navigateBooking(t.tid)}}>Book</button>
                            </Col>
                            <Col>
                            <button className="btn btn-success">About</button>
                            </Col>
                        </Row>
                        
                    </Card>
                ))
                }
            </Row>
            <Row>
                <h2>My Order ⚒
                <button className="btn btn-primary w-2">Refresh</button>
                </h2>
                {myorderlist.map((o) => (
                    <Card className="m-2 w-25 h-25" key={o.order_id}>
                        <CardTitle>{o.service_type}</CardTitle>
                        <CardText>💨{o.status}</CardText>
                        <button className="btn btn-success w-2" onClick={()=>{navigateOrderDetail(o.order_id)}}>Detail</button>
                    </Card>
                ))}

            </Row>
            <Row>
                <h2>My Pet 🐶        
                <button className="btn btn-primary m-auto" onClick={navigateAddPet}>Add pet</button>
                </h2>
                {mypetlist.map((pet) => (
                    <Card key={pet.pid} className="m-2 w-25 h-25">
                        <CardTitle>{pet.p_name}</CardTitle>
                        <CardText>{pet.species}</CardText>
                        <CardText>{pet.breed}</CardText>
                        <button className="btn btn-primary w-2" onClick={() =>{navigatePetView(pet.pid)}}>See more</button>
                    </Card>
                ))}

                <button className="btn btn-danger" onClick={() => {navigate("/")}}>Log Out</button>
            </Row>
        </div>
        
    );
}
export default PetOwnerHome;