import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
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
    </Routes>
  );
}

export default App;