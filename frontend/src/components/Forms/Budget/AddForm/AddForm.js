import React, {useEffect} from "react";
import {useState} from "react";


const AddBudgetForm = ({access, user}) => {
    const [name, setName] = useState(0);

        let handleAddBudget = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://127.0.0.1:8000/api/budget/", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${access}`
                },
                body: JSON.stringify({
                    user: user,
                    name: name
                }),
            }).then(response => {
                window.location.reload(false)
            });
        } catch (err) {
            console.log(err);
        }
    };


    return (
        <div className="modal">
            <form className="form">
                <div className="input-group">
                    <label htmlFor="name">name</label>
                    <input type="text" name="name" placeholder="name"
                           onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <button className="primary" onClick={handleAddBudget}>Add budget</button>
            </form>
        </div>
    )
}

export default AddBudgetForm;