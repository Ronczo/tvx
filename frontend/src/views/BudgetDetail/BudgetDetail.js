import React, {useEffect, useState} from "react";
import "./BudgetDetail.css"
import AddForm from "../../components/AddForm/AddForm";

const BudgetDetail = () => {
    const accessToken = localStorage.getItem("access")
    const split_url = window.location.href.split("/")
    const itemID = split_url[split_url.length - 1];
    const [item, setItem] = useState({});
    const [transactions, setTransactions] = useState([]);
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
                let res = fetch(`http://127.0.0.1:8000/api/budget/${itemID}`, {
                    method: "GET",
                    headers: {
                        Authorization: `Bearer ${accessToken}`
                    }
                }).then(response => response.json()).then(data => {
                    setItem(data)
                    setTransactions(data.transactions)
                    console.log(data.transactions)
                });
            } catch (err) {
                console.log(err);
            }
        }
    }, []);

    const deleteTransaction = async (transactionID) => {
        try {
            let res = await fetch(`http://127.0.0.1:8000/api/transaction/${transactionID}/`, {
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


        return (
            <div>
                <div>
                    <h2>{item.name}</h2>
                    <h3>Balance: {item.balance}</h3>
                    <h3>Transactions:</h3>
                    {modalOpen ? <button onClick={closeModal}>Hide form</button> :
                        <button className={"addButton"} onClick={openModal}>Add transaction</button>}
                    {modalOpen ? <AddForm budgetID={itemID} access={accessToken}/> : ""}
                    {transactions.map(transaction => (
                        <>
                            <p key={`transaction-${transaction.id}`}>Category: {transaction.category}</p>
                            <p key={`transaction-${transaction.id}`}>Kind: {transaction.kind}</p>
                            <p key={`transaction-${transaction.id}`}>Value: {transaction.value}</p>
                            <button className={"deleteButton"} onClick={() => deleteTransaction(transaction.id)}>Delete transaction</button>
                            <hr/>
                        </>
                    ))}
                </div>
            </div>
        )
    }

    export default BudgetDetail;
