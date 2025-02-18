import { useLocation, useNavigate } from "react-router-dom";

export default function AudioPlayerPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { audioUrl } = location.state || {};  // ✅ Extract the URL from navigation state

    console.log("🎵 Received Audio URL:", audioUrl);

    if (!audioUrl) {
        return (
            <div className="error-container">
                <h1>Error: No audio found. Please upload a file first.</h1>
                <button onClick={() => navigate("/")}>Go Back</button>
            </div>
        );
    }

    return (
        <div className="audio-container">
            <h1>AI-Generated Lecture</h1>
            <audio controls autoPlay>
                {/* ✅ Use audioUrl directly, since it's already a full URL */}
                <source src={audioUrl} type="audio/mpeg" />
                Your browser does not support the audio element.
            </audio>
            <br />
            <button onClick={() => navigate("/")}>Upload Another File</button>
        </div>
    );
}
