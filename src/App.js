import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import ReactDOM from "react-dom/client";
import React from "react";
import Login from "./Login";
// import Signup from "./Signup";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={Login} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
