import { Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
    const navigate = useNavigate();

    const handleLogIn = (user_type) =>{
        navigate(`/login/${user_type}`)
    };
    const handleSignUpPetOwner = () =>{
        navigate('/petowner-register');
    };
    const handleSignUpTrainer = () =>{
        navigate('/trainer-register');
    };
    const handleSignUpProvider = () =>{
        navigate('/provider-register');
    };
    return (
        <Container fluid className='d-flex flex-column justify-content-center align-items-center' style={{ minHeight: '100vh' }}>
            <p className="h1 text-center mb-5">🐱🐶Welcome to PetXercise🐰🐹</p>
            <div className="w-100 mb-4 text-center" style={{ backgroundColor:'#EEE2D1'}}>
                <Col className="p-3 mx-auto" >
                    <p className="h1">🐈Pet Owner🐕</p>
                    <button type="button" className="btn btn-success me-5" onClick={()=>handleLogIn("user")}>Log In</button>
                    <button type="button" className="btn btn-primary" onClick={handleSignUpPetOwner}>Sign Up</button>
                </Col>
            </div>
            <div className="w-100 mb-4 text-center" style={{ backgroundColor: '#EEE2D1'}}>
                <Col className="p-3 mx-auto" >
                    <p className="h1">👟Trainer👟</p>
                    <button type="button" className="btn btn-success me-5" onClick={()=>handleLogIn("trainer")}>Log In</button>
                    <button type="button" className="btn btn-primary" onClick={handleSignUpTrainer}>Sign Up</button>
                </Col>
            </div>
            <div className="w-100 mb-4 text-center" style={{ backgroundColor: '#EEE2D1'}}>
                <Col className="p-3 mx-auto" >
                    <p className="h1">💼Provider💼</p>
                    <button type="button" className="btn btn-success me-5" onClick={()=>handleLogIn("provider")}>Log In</button>
                    <button type="button" className="btn btn-primary" onClick={handleSignUpProvider}>Sign Up</button>
                </Col>
            </div>
        </Container>
    );
}

export default LandingPage;
