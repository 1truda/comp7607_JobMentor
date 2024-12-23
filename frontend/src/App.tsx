import React from 'react';
import './App.css';
import Header from './component/Header';
import { Outlet } from 'react-router-dom';

function App() {
    return (
        <div className="container">
            <div className='right'>
                <Header></Header>
                <div className='main'><Outlet /></div>
            </div>
        </div>
    );
}

export default App;

