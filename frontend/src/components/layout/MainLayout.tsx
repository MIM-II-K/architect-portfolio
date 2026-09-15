import { Outlet } from "react-router-dom";

import Header from "../navigation/Header";
import Footer from "./Footer";

function MainLayout() {
  return (
    <div className="site">
      <Header />

      <main className="site-main">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}

export default MainLayout;