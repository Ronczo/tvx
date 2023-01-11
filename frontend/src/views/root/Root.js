import React, {useState} from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Header from "../../components/header/Header";
import LoginPanel from "../../components/loginPanel/loginPanel";
import Home from "../home/Home";

const Root = () => {


    return (
        <BrowserRouter>
            <Header/>
            <LoginPanel />
            <Routes>
                {/*<Route path="/" element={<Home/>}/>*/}
                {/*<Route path="/notes" element={<NotesView/>}/>*/}
            </Routes>
        </BrowserRouter>
    );

}

export default Root;
