import { createBrowserRouter } from "react-router-dom";
import Home from "@/pages/Home";
import ProjectDetails from "@/pages/ProjectDetails";
import CreateSrChat  from "@/pages/srcreate/CreateSrChat";
import App from "@/App";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // layout here
    children: [
      { path: "/", element: <Home /> },
      { path: "/domain/:pathUrl", element: < CreateSrChat/> },
    ],
  },
]);

