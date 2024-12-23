import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {createBrowserRouter, RouterProvider} from "react-router-dom";


import ExamPage from "./modules/exam/ExamPage";
import InterviewPage from "./modules/interview/InterviewPage";
import SchedulePage from "./modules/schedule/SchedulePage";


// @ts-ignore
const router = createBrowserRouter([
  {
    path:'/',
    element: <App />,
    children: [
      {
        index: true, element: <ExamPage />
      },
      {
        path: "/index/ExamPage",
        element: <ExamPage />
      },
      {
        path: "/index/InterviewPage",
        element: <InterviewPage />
      },
      {
        path: "/index/SchedulePage",
        element: <SchedulePage />
      },



    ],
  },
])
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
    <RouterProvider router={router} />
);
reportWebVitals();
