import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { UploadPage } from "./src/components/UploadPage";
import { AudioPage } from "AudioPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/audio" element={<AudioPage />} />
      </Routes>
    </Router>
  );
}

export default App;
