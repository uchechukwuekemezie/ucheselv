import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import ReactDOM from "react-dom/client";
import React from "react";
import Login from "./Login";
import Signup from "./Signup";
import Header from "./Header";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/Signup" element={<Signup />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
