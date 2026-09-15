import { Route, Routes } from "react-router-dom";

import MainLayout from "./components/layout/MainLayout";

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route
          path="/"
          element={<div>Home</div>}
        />

        <Route
          path="/about"
          element={<div>About</div>}
        />

        <Route
          path="/projects"
          element={<div>Projects</div>}
        />

        <Route
          path="/projects/:slug"
          element={<div>Project Detail</div>}
        />

        <Route
          path="/contact"
          element={<div>Contact</div>}
        />

        <Route
          path="*"
          element={<div>404 - Page Not Found</div>}
        />
      </Route>
    </Routes>
  );
}

export default App;