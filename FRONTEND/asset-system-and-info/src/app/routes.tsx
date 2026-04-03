import { createBrowserRouter } from "react-router-dom";
import Home from "@/pages/Home";
import ProjectDetails from "@/pages/ProjectDetails";
import CreateSrChat  from "@/pages/srcreate/CreateSrChat";
import App from "@/App";
import SystemCheckScreen from "@/pages/system/SystemCheckScreen";
import DynamicDomain from "./dynamicdomain";
import SrDataGrid from "@/pages/srcreate/SrDataGrid";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, // layout here
    children: [
      { path: "/", element: <Home /> },
      { path: "/domain/:pathUrl", element: < DynamicDomain/> },
      {path : "/system" ,element : <SystemCheckScreen/>},
      {path : "/service-requests" ,element : <SrDataGrid/>}

    ],
  }
]);

