import { useEffect, useState } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useNavigate, useParams } from "react-router-dom";
import axios
 from "axios";
function Payment(){
    const navigate = useNavigate();
    const [payment, setPayment] = useState('');
    const {oid, uid, tid, session_token} = useParams();
    const [uemail, setUemail] = useState('');
    const get_user_ep = `${import.meta.env.VITE_USER}`;
    const make_payment_ep = `${import.meta.env.VITE_PAYMENT}`;
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

    async function handlePay(e){
        e.preventDefault();
        const dataToSend = {
            data:{
                "payment":{
                    "order_id":Number(oid),
                    "payment_info" : payment
                }
            }
        }

        try{
            const response = await axios.post(make_payment_ep, dataToSend, {
                headers: {
                    'token': session_token,
                },
                withCredentials: true,
            })
            alert("Payment successful!");
            navigate(`/phome/${uemail}/${session_token}`)
        }catch (error){
            console.error("Problem with paying order:", error);
            alert("Problem with paying order.");
        }
    }
    function handleCancel(){
        navigate(`/phome/${uemail}/${session_token}`)
    }
    return(
        <div>
        <p className="h1 text-center mb-5">Payment 💲</p>
        <Container>
            <form onSubmit={handlePay}>
                <Row>
                    <Col>
                    <div className="mb-3">
                                    <label className="form-label">Payment
                                    <input type="text" className="form-control" id="p_name" value={payment} onChange={(e) => setPayment(e.target.value)} required/>
                                    </label>
                                </div>
                    </Col>
                </Row>
                <button type="submit" className="btn btn-success">Pay</button>
                <button type="button" className="btn btn-danger" onClick={handleCancel}>Cancel</button>
            </form>
        </Container>
        </div>
        
    );
}
export default Payment;