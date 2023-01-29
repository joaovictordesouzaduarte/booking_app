import React from "react";
import { useState, useContext } from "react";
import AuthContext from "../../context/AuthContext";
import axios from "axios";

import "./login.css";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const BASE_URL = "http://localhost:8000";

  const [credentials, setCredentials] = useState({
    username: undefined,
    password: undefined,
  });

  const { user, loading, error, dispatch } = useContext(AuthContext);
  const navigate = useNavigate()
  const handleChange = (e) => {
    setCredentials((prev) => ({ ...prev, [e.target.id]: e.target.value }));
  };

  const handleClick = async (e) => {
    e.preventDefault();

    dispatch({ type: "LOGIN_START" });
    try {
      const res = await axios.post(`${BASE_URL}/login`, credentials, {
        headers: {
          "accept": "application/json",
          "Content-Type": "application/json",
        },
      });
      dispatch({ type: "LOGIN_SUCCESS", payload: res.data });
      navigate('/')
    } catch (err) {
      dispatch({ type: "LOGIN_FAILURE", payload: err.response.data.detail });
    }
  };

  return (
    <div className="login">
      <div className="lContainer">
        <input
          type="text"
          placeholder="username"
          id="username"
          onChange={handleChange}
          className="lInput"
        />
        <input
          type="password"
          id="password"
          className="lInput"
          placeholder="password"
          onChange={handleChange}
        />
        <button disabled={loading} onClick={handleClick} className="lButton">
          Login
        </button>
        {error && <span>{error}</span>}

      </div>
    </div>
  );
};

export default Login;
