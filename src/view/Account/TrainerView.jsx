import { useNavigate } from "react-router-dom";

function TrainerView(){
    const navigate = useNavigate();
    return(
        <button onClick={() => {navigate(-1)}}>Back</button>
    );
}
export default TrainerView;