import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UploadPage from "./components/UploadPage";
import ViewerPage from "./components/ViewerPage";

export default function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<UploadPage />} />
                <Route path="/viewer" element={<ViewerPage />} />
            </Routes>
        </Router>
    );
}
