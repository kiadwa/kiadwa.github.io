import { useState } from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { LandingPage,
  TrainerHome,
  LogIn,
  PetOwnerHome,
  RegisterPetOwner,
  RegisterTrainer, 
  PetSignUp,
  ProviderRegister,
  MakeOrder,
  Payment,
  ServiceView,
  PetHelpAIView,
  PetView,
  TrainerView,
  PetOwnerChangeInfo,
  TrainerChangeInfo,
} from './view/import';
import ProviderHome from './view/Account/ProviderHome';

function App() {
  return(
    <Router>
      <div className='App'>
        <Routes>
          <Route path="/" element={<LandingPage/>}/>
          <Route path="/login/:user_type" element={<LogIn/>}/>
          {/*Register*/}
          <Route path="/petowner-register" element={<RegisterPetOwner/>}/>
          <Route path="/trainer-register" element={<RegisterTrainer/>}/>
          <Route path="/provider-register" element={<ProviderRegister/>}/>
          {/*Home page*/}
          <Route path= "/phome/:email/:session_token" element={<PetOwnerHome/>}/>
          <Route path= "/thome/:email/:session_token" element={<TrainerHome/>}/>
          <Route path= "/provhome/:email/:session_token" element={<ProviderHome/>}/>
          <Route path= "/trainer-view/:tid/:uid/:session_token" element={<TrainerView/>}/>
          <Route path="/user-update/:uid/:session_token" element={<PetOwnerChangeInfo/>} />
          <Route path="/trainer-update/:tid/:session_token" element={<TrainerChangeInfo/>}/>
          {/*Pet*/}
          <Route path="/pet-register/:uid/:session_token" element={<PetSignUp/>}/>
          <Route path="/pet/:pid/:uid/:session_token" element={<PetView/>}/>
          <Route path="/pethelp/:pid/:uid/:session_token" element={<PetHelpAIView/>}/>
          {/*Order*/}
          <Route path="/order/:tid/:uid/:session_token" element={<MakeOrder/>}/>
          <Route path="/payment/:oid/:uid/:tid/:session_token" element={<Payment/>}/>
          <Route path="/service/:oid/:uid/:session_token" element={<ServiceView/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App
