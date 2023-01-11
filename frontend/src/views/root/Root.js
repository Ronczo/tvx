import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "../../components/header/Header";
import LoginPanel from "../../components/loginPanel/loginPanel";

class Root extends React.Component {


    render() {
        return (
            <BrowserRouter>
                <Header/>
                <LoginPanel/>
                    {/*<Routes>*/}
                    {/*    /!*<Route path="/articles" element={<ArticlesView/>}/>*!/*/}
                    {/*    /!*<Route path="/notes" element={<NotesView/>}/>*!/*/}
                    {/*</Routes>*/}
            </BrowserRouter>
        );
    }
}

export default Root;
