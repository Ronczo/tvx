import React, {useEffect} from "react";
import {useState} from "react";
import "./loginPanel.css";
import logout from "../../api/logout";
import jwt_decode from "jwt-decode";

const LoginPanel = () => {
    const access_token = localStorage.getItem("access")
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [access, setAccess] = useState(access_token);
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (access_token) {
            const decoded = jwt_decode(access_token)
            const user_id = decoded["user_id"]
            try {
                let res = fetch(`http://127.0.0.1:8000/auth/user/${user_id}`, {
                    method: "GET",
                }).then(response => response.json()).then(data => {
                    setUsername(data["username"])
                });
            } catch (err) {
                console.log(err);
            }
        }
    }, []);

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
                return response.json()
            }).then((data) => {
                localStorage.setItem('access', data["access"]);
                localStorage.setItem('refresh', data["refresh"]);
                setAccess(data["access"])
                window.location.reload(false)
            });
        } catch (err) {
            console.log(err);
        }
    };


    if (!access) {
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
        )
            ;
    } else {
        return (
            <div className="userInfo">
                <p>Welcome <b>{username}</b></p>
                <button type="submit" className="secondary" onClick={logout}>Logout</button>
            </div>
        )
    }
}

export default LoginPanel;