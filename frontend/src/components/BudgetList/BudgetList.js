import React, {useEffect, useState} from "react";
import "./BudgetList.css"

import {NavLink} from "react-router-dom";

import AddBudgetForm from "../Forms/Budget/AddForm/AddForm";
import jwt_decode from "jwt-decode";
import ShareForm from "../Forms/Budget/ShareForm/ShareForm";

const BudgetList = () => {
    const accessToken = localStorage.getItem("access")
    const [budgets, setBudgets] = useState([]);
    const [sharedBudgets, setSharedBudgets] = useState([]);
    const [nextPage, setNextPage] = useState("");
    const [previousPage, setPreviousPage] = useState("");
    const [modalOpen, setModalOpen] = useState(false);
    const [modalShareOpen, setModalShareOpen] = useState(false);
    const [users, setUsers] = useState([]);
    const [filterCategory, setFilterCategory] = useState("");


    const openModal = () => {
        setModalOpen(true)
    }

    const closeModal = () => {
        setModalOpen(false)
    }

    const openShareModal = () => {
        setModalShareOpen(true)
    }

    const closeShareModal = () => {
        setModalShareOpen(false)
    }


    const handleFilter = async (e) => {
        e.preventDefault();
        try {
            let res = fetch(`http://127.0.0.1:8000/api/budget/my-budgets?category=${filterCategory}`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            }).then(response => response.json()).then(data => {
                setBudgets(data["results"])
                console.log(data)
            });
        } catch (err) {
            console.log(err);
        }
    }

    const deleteBudget = async (budgetID) => {
        try {
            let res = await fetch(`http://127.0.0.1:8000/api/budget/${budgetID}/`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${accessToken}`
                },
            }).then(response => {
                window.location.reload(false)

            });
        } catch (err) {
            console.log(err);
        }
    }

    useEffect(() => {

        if (accessToken) {
            try {
                let res = fetch(`http://127.0.0.1:8000/api/budget/my-budgets?${filterCategory}`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${accessToken}`
                    }
                }).then(response => response.json()).then(data => {

                    setBudgets(data["results"])
                });
            } catch (err) {
                console.log(err);
            }
            try {
                let res = fetch(`http://127.0.0.1:8000/api/budget/shared-with-me/`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${accessToken}`
                    },
                }).then(response => response.json()).then(data => {
                    setSharedBudgets(data["results"])
                });
            } catch (err) {
                console.log(err);
            }
        }

        try {
            let res = fetch(`http://127.0.0.1:8000/auth/user`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            }).then(response => response.json()).then(data => {
                setUsers(data)
                console.log(data)
            });
        } catch (err) {
            console.log(err);
        }

    }, []);

    if (!accessToken) {
        return (
            <div className={"notLogged"}>
                <p>Log in first</p>
            </div>
        )
    } else {
        const decoded = jwt_decode(accessToken)
        const user_id = decoded["user_id"]
        return (
            <div className={"listWrapper"}>
                <div className={"list"}>

                    <p className={"tableHeader"}>Your budgets:</p>
                    {modalOpen ? <button onClick={closeModal}>Hide form</button> :
                        <button className={"addButton"} onClick={openModal}>Add budget</button>}
                    {modalOpen ? <AddBudgetForm access={accessToken} user={user_id}/> : ""}
                    <form className="form">
                        <div className="input-group">
                            <label htmlFor="user">find by category in transactions</label>
                            <input type="text" name="filterCategory" placeholder="filterCategory"
                                   onChange={(e) => setFilterCategory(e.target.value)}
                            />
                        </div>
                        <button className="primary" onClick={handleFilter}>Filter budgets</button>
                    </form>
                    {budgets.map(item => (

                        <>
                            <p key={`item-${item.id}`} className={"item"}>- {item.name} (balance: {item.balance})
                                <br/>
                                <NavLink className={"navLink"} to={`/budget-details/${item.id}`}>Show</NavLink>
                                <button className={"deleteButton"} onClick={() => deleteBudget(item.id)}>Delete</button>
                                {modalShareOpen ? <button onClick={closeShareModal}>Hide form</button> :
                                    <button className={"addButton"} onClick={openShareModal}>Share budget</button>}
                                {modalShareOpen ? <ShareForm users={users} access={accessToken} budget={item.id}/> : ""}
                            </p>
                        </>
                    ))}
                </div>

                <div className={"list"}>
                    <p className={"tableHeader"}>Budgets shared with you:</p>
                    {sharedBudgets.map(item => (

                        <>
                            <p key={`item-${item.id}`}
                               className={"item"}>- {item.name} (balance: {item.balance})<br/>[Belongs to {item.user}]
                                <br/>
                                <NavLink className={"navLink"} to={`/budget-details/${item.id}`}>Show</NavLink>
                                <button className={"deleteButton"} onClick={() => deleteBudget(item.id)}>Delete</button>

                            </p>
                        </>
                    ))}
                </div>
            </div>
        )
    }
}


export default BudgetList