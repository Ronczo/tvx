import React from "react";
import {useState} from "react";
import "./loginPanel.css";

const LoginPanel = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    let handleRegistration = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://127.0.0.1:8000/auth/user/", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
            }).then(response => {
                setMessage("User created")
            });
        } catch (err) {
            console.log(err);
        }
    };

    let handleLogin = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://127.0.0.1:8000/auth/login/", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
            }).then(response => {
                if (response.status === 200) {
                    setMessage("You're logged in")
                } else {
                    setMessage("Something went wrong")
                }
            });
        } catch (err) {
            console.log(err);
        }
    };


    return (
        <div className="loginPanel">
            <form className="form">
                <div className="input-group">
                    <label htmlFor="email">Username</label>
                    <input type="text" name="username" placeholder="username"
                           onChange={(e) => setUsername(e.target.value)}/>
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password" placeholder="password"
                           onChange={(e) => setPassword(e.target.value)}/>
                </div>
                <button className="primary" onClick={handleLogin}>Login</button>
            </form>
            <button type="submit" className="secondary" onClick={handleRegistration}>
                Create account
            </button>
            <div className="message">{message ? <p>{message}</p> : null}</div>
        </div>
    );
}


export default LoginPanel;