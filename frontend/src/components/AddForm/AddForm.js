import React, {useEffect} from "react";
import {useState} from "react";
import "./AddForm.css"

const AddForm = ({budgetID, access}) => {
    const [value, setValue] = useState(0);
    const [kind, setKind] = useState("");
    const [category, setCategory] = useState("");

        let handleAddTransaction = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://127.0.0.1:8000/api/transaction/", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${access}`
                },
                body: JSON.stringify({
                    kind: kind,
                    category: category,
                    budget: budgetID,
                    value: value,
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
                    <label htmlFor="value">Value</label>
                    <input type="text" name="value" placeholder="value"
                           onChange={(e) => setValue(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="category">category</label>
                    <input type="text" name="category" placeholder="category"
                           onChange={(e) => setCategory(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="kind">kind</label>
                    <select onChange={(e) => setKind(e.target.value)}>

                        <option disabled selected value> -- select an option -- </option>
                        <option value="income">income</option>
                        <option value="expanse">expanse</option>
                    </select>
                </div>
                <button className="primary" onClick={handleAddTransaction}>Add transaction</button>
            </form>

            {/*<div className="message">{message ? <p>{message}</p> : null}</div>*/}
        </div>
    )
}

export default AddForm;