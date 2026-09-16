import { Outlet } from "react-router-dom";

import Header from "../navigation/Header";
import Footer from "./Footer";

export default function MainLayout() {
  return (
    <div className="site">
      <Header />

      <main>
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}