import React from "react";
import { BrowserRouter, Routes } from "react-router-dom";
import Header from "../../components/header/Header";

class Root extends React.Component {


    render() {
        return (
            <BrowserRouter>
                <Header/>
                    <Routes>
                        {/*<Route path="/" element={<TwittersView/>}/>*/}
                        {/*<Route path="/articles" element={<ArticlesView/>}/>*/}
                        {/*<Route path="/notes" element={<NotesView/>}/>*/}
                    </Routes>
            </BrowserRouter>
        );
    }
}

export default Root;
