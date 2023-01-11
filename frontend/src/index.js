import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

import reportWebVitals from './files_to_delete/reportWebVitals';
import Root from "./views/root/Root";

const container = document.getElementById("root")
const root = ReactDOM.createRoot(container)
root.render(<Root />)
reportWebVitals();
