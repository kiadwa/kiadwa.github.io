import { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';

function PetSignUp(){
    const navigate = useNavigate();
    const [p_name, setP_name] = useState('');
    const [species, setSpecies] = useState('');
    const [breed, setBreed] = useState('');
    const [age, setAge] = useState();
    const [diagnosis, setDiagnosis] = useState('');
    const [dob, setDob] = useState('');
    const [uemail, setUemail] = useState('');
    const {uid, session_token}  = useParams();
    const pet_ep=`${import.meta.env.VITE_PET}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`

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

    const handleSubmit = async(e) => {
        e.preventDefault();
        let currTime = new Date().toISOString().split("T")[1]
        let timestamp = `${dob}T${currTime}`;
        let date = new Date(timestamp);
        let time = date.getTime() / 1000;
        const dataToSend = {
            data:{
                "pet" : {
                    "p_name": p_name,
                    "species": species,
                    "breed" : breed,
                    "age" : Number(age),
                    "uid" : uid,
                    "diagnosis" : diagnosis,
                    "dob" : time
                }
            }
        }
        console.log(dataToSend);
        try{
            const response = await axios.post(pet_ep, dataToSend,{
                headers:{
                    'token':session_token
                }
            });
            console.log(response);
            alert("Pet registered")

        }catch(error){
            console.log("Error", error);
        }

        handleCancel();
    }
    const handleCancel = () =>{
        navigate(`/phome/${uemail}/${session_token}`);
    }
    return(
        <div >
            <p className="h1 text-center mb-5">Pet Sign Up 🐕</p>
            <Container style={{ minHeight: '100vh' }}>
            <form onSubmit= {handleSubmit}>
            <Row>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Pet Name</label>
                    <input type="text" className="form-control" id="p_name" value={p_name} onChange={(e) => setP_name(e.target.value)} required/>
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Species</label>
                    <select className="form-select" aria-label="Default select example" value={species} onChange={(e) => setSpecies(e.target.value)} required>
                            <option defaultValue={''}>Select your pet's species</option>
                            <option value="Canine">Dog</option>
                            <option value="Feline">Cat</option>
                            <option value="Rodent">Rodent</option>
                            <option value="Fish">Fish</option>
                            <option value="Insect">Insect</option>
                            <option value="Reptilian">Reptilian</option>
                            </select>
                </div>
                </Col>
                </Row>
                <Row>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Breed</label>
                    <input type="text" className="form-control" id="breed" value={breed} onChange={(e) => setBreed(e.target.value)} required/>
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">DOB</label>
                    <input type="date" className="form-control" id="dob" value={dob} onChange={(e) => setDob(e.target.value)} />
                </div>
                </Col>
                <Col>
                <div className="mb-3">
                    <label className="form-label">Age</label>
                    <input type="number" className="form-control" id="age" value={age} onChange={e => setAge(e.target.value)}/>
                </div>
                </Col>
                </Row>
                <Row>
                <div className="mb-3">
                    <label className="form-label">Diagnosis</label>
                    <input type="text" className="form-control" id="diagnosis" value={diagnosis} onChange={(e) => setDiagnosis(e.target.value)}/>
                </div>
                </Row>
                <button type="submit" className="btn btn-primary me-2" >Sign Up</button>
                <button type="cancel" className="btn btn-danger me-2 " onClick={handleCancel}>Cancel</button>
            </form>
            </Container>
        </div>
    );
}
export default PetSignUp;