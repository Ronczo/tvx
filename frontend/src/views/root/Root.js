import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Header from "../../components/header/Header";
import LoginPanel from "../../components/loginPanel/loginPanel";
import Home from "../home/Home";

const Root = () => {
    return (
            <BrowserRouter>
                    <Header/>
                    <LoginPanel />
                    <div className={"wrapper"}>
                        <Routes>
                            <Route path="/" element={<Home/>}/>
                        </Routes>
                    </div>
            </BrowserRouter>
    );
}

export default Root;
