import React, {useEffect} from "react";
import {useState} from "react";
import {NavLink} from "react-router-dom";


const ShareForm = ({access, budget, users}) => {
    const [user, setUser] = useState("");


    let handleShareBudget = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://127.0.0.1:8000/api/budget/share/", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${access}`
                },
                body: JSON.stringify({
                    budget: budget,
                    user: user
                }),
            }).then(response => {
                window.location.reload(false)
            });
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {

    }, []);


    return (
        <div className="modal">
            <form className="form">
                <div className="input-group">
                    <label htmlFor="user">name</label>
                    <select onChange={(e) => setUser(e.target.value)}>
                        <option disabled selected value> -- select an option --</option>
                        {users.map(item => (
                            <>
                                <option value={item.id}>{item.username}</option>
                            </>
                        ))


                        }
                    </select>
                </div>
                <button className="primary" onClick={handleShareBudget}>Share budget</button>
            </form>
        </div>
    )
}

export default ShareForm;