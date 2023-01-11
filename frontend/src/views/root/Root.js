import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Header from "../../components/header/Header";
import LoginPanel from "../../components/loginPanel/loginPanel";
import Home from "../home/Home";
import "./Root.css"


const Root = () => {
    return (
        <BrowserRouter>
            <Header/>
            <div className={"wrapper"}>
                <LoginPanel/>

                <Routes>
                    <Route path="/" element={<Home/>}/>
                </Routes>

            </div>

        </BrowserRouter>
    );
}

export default Root;
