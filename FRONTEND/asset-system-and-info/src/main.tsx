import { createRoot } from 'react-dom/client'
import './globals.css'
import React from 'react'
import { RouterProvider } from "react-router-dom";
import { router } from "./app/routes";

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
  <RouterProvider router={router} />
</React.StrictMode>
)
