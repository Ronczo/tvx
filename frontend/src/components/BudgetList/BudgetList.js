import React, {useEffect, useState} from "react";
import "./BudgetList.css"
import jwt_decode from "jwt-decode";

const BudgetList = () => {
    const accessToken = localStorage.getItem("access")
    const [access, setAccess] = useState(accessToken);
    const [budgets, setBudgets] = useState(accessToken);

    useEffect(() => {

        if (accessToken) {
            try {
                let res = fetch(`http://127.0.0.1:8000/api/budget/my-budgets`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${access}`
                    }
                }).then(response => response.json()).then(data => {
                    console.log(data)
                    setBudgets(data)
                });
            } catch (err) {
                console.log(err);
            }
        }
    }, []);

    if (!access) {
        return (
            <div className={"notLogged"}>
                <p>Log in first</p>
            </div>
        )
    } else {
        return (

            <div className={"list"}>
                <p className={"row"}>asd</p>
            </div>
        )
    }
}


export default BudgetList