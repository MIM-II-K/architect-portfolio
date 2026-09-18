import { Outlet, useLocation } from "react-router-dom";
import { useEffect } from "react";
import Header from "../navigation/Header"; // Your custom Header component
import Footer from "./Footer";
import "../../styles/MainLayout.css";

export default function MainLayout() {
  const location = useLocation();

  // Automatically scroll to top on route change for smooth UX
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [location.pathname]);

  return (
    <div className="site-wrapper">
      {/* Dynamic Header Component with integrated mobile drawer and glassmorphism */}
      <Header />

      {/* Main content wrapper with a fade-in key property reset on route change */}
      <main className="site-main" key={location.pathname}>
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}