import React, {useEffect, useState} from "react";
import "./BudgetList.css"

import {NavLink} from "react-router-dom";

const BudgetList = () => {
    const accessToken = localStorage.getItem("access")
    const [access, setAccess] = useState(accessToken);
    const [budgets, setBudgets] = useState([]);
    const [nextPage, setNextPage] = useState("");
    const [previourPage, setPreviousPage] = useState("");

    useEffect(() => {

        if (accessToken) {
            try {
                let res = fetch(`http://127.0.0.1:8000/api/budget/my-budgets`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${access}`
                    }
                }).then(response => response.json()).then(data => {
                    setBudgets(data["results"])
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
            <div className={"listWrapper"}>
                <div className={"list"}>
                    <p className={"tableHeader"}>Your budgets:</p>
                    {budgets.map(item => (

                        <>
                            <p key={`item-${item.id}`} className={"item"}>- {item.name}
                                <NavLink className={"navLink"} to={`/budget-details/${item.id}`}>Show</NavLink>
                            </p>
                        </>
                    ))}
                </div>

                <div className={"list"}>
                    <p>Budgets shared with you:</p>
                    <p className={"row"}>TU BEDZIE TABELA</p>
                </div>
            </div>
        )
    }
}


export default BudgetList