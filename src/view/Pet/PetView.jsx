import { useState, useEffect } from "react";
import { Container, Row, Col, CardBody } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
function PetView(){
    const navigate = useNavigate();
    const {pid, uid, session_token} = useParams();
    const [pet, setPet] = useState({});
    const [uemail, setUemail] = useState('');
    const get_pet_ep=`${import.meta.env.VITE_PET}`;
    const get_user_ep = `${import.meta.env.VITE_USER}`;
    const get_pet_avatar_url = `${import.meta.env.VITE_PET_AVATAR}`;
    const upload_file_ep = `${import.meta.env.VITE_VITE_UPLOAD}`;
    
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

    useEffect(() => {
        if (uid) {
            let isMounted = true;

            async function fetch_my_pet_list() {
                try {
                    const response = await axios.get(`${get_pet_ep}?pid=${pid}`, {
                        headers: {
                            'token': session_token
                        }
                    });
                    if (isMounted) {
                        setPet(response.data.data.pet_list[0]);
                    }
                } catch (error) {
                    if (isMounted) {
                        console.error("Error fetching pet list:", error);
                    }
                }
            }
            fetch_my_pet_list();

            return () => {
                isMounted = false;
            };
        }
    }, [uid, session_token]);

    function handlePetHelpAI(){
        navigate(`/pethelp/${pid}/${uid}/${session_token}`);
    }
    function handleCancel(){
        navigate(`/phome/${uemail}/${session_token}`);
    }
    return(
        <div>                
            <Container>
                <p className="h1 text-center mb-5">My Pet 🐶</p>
                <form >
                    <Row>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Pet name
                                    <input type="text" className="form-control" id="p_name" defaultValue={pet.p_name} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Species
                                    <input type="text" className="form-control" id="species" defaultValue={pet.species} readOnly />
                                </label>
                            </div>
                        </Col>
                        <Col>
                            <div className="mb-3">
                                <label className="form-label">Breed
                                    <input type="text" className="form-control" id="breed" defaultValue={pet.breed} readOnly />
                                </label>
                            </div>
                        </Col>
                    </Row>
                    <Row>
                    </Row>
                    <Row>
                            <div className="mb-10">
                                <label className="form-label">Diagnosis
                                    <input type="text" className="form-control w-100" id="service" defaultValue={pet.diagnosis} onChange={(e) => { }} />
                                </label>
                            </div>
                    </Row>
                    <button type="button" className="btn btn-primary me-2" onClick={handlePetHelpAI}>Pet Help AI</button>
                    <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
                </form>
            </Container>
        </div>
    );
}
export default PetView;