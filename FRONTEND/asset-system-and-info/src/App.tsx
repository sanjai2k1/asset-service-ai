import { Header } from "@/components/common/Header";
import { Toaster } from "@/components/ui/toaster";
import { Outlet } from "react-router-dom";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col font-body antialiased">
      <Header />

      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>

      <Toaster />
    </div>
  );
}