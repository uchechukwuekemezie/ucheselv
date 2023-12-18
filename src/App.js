import "./App.css";
import Login from "./Login";
import Signup from "./Signup";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/src/Signup.js" component={Signup} />
          <Route path="/src/Login.js" component={Login} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
