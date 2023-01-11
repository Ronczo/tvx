import React, {useEffect, useState} from "react";
import "./BudgetList.css"

import {NavLink} from "react-router-dom";

import AddBudgetForm from "../Forms/Budget/AddForm/AddForm";
import jwt_decode from "jwt-decode";

const BudgetList = () => {
    const accessToken = localStorage.getItem("access")
    const [access, setAccess] = useState(accessToken);
    const [budgets, setBudgets] = useState([]);
    const [nextPage, setNextPage] = useState("");
    const [previousPage, setPreviousPage] = useState("");
    const [modalOpen, setModalOpen] = useState(false);



    const openModal = () => {
        setModalOpen(true)
    }

    const closeModal = () => {
        setModalOpen(false)
    }

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
            const decoded = jwt_decode(access)
            const user_id = decoded["user_id"]
        return (
            <div className={"listWrapper"}>
                <div className={"list"}>
                    <p className={"tableHeader"}>Your budgets:</p>
                    {modalOpen ? <button onClick={closeModal}>Hide form</button> :
                        <button className={"addButton"} onClick={openModal}>Add transaction</button>}
                    {modalOpen ? <AddBudgetForm access={access} user={user_id}/> : ""}
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