import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPage() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleUpload = async () => {
        if (!file) return alert("Please select a PDF or PPTX");

        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);
        setError(null);

        try {
            console.log("🚀 Uploading file...");
            const response = await fetch("http://127.0.0.1:8080/upload", {
                method: "POST",
                body: formData,
            });

            console.log("📩 Raw Response:", response);

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            // ✅ Check if response is JSON before parsing
            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                throw new Error("Invalid response format (not JSON)");
            }

            const data = await response.json();
            console.log("📩 Parsed Response:", data);

            if (data.audio_url) {
                console.log("📩 Navigating to /audio with URL:", data.audio_url);
                navigate("/audio", { state: { audioUrl: data.audio_url } });  // ✅ Correct format
            } else {
                throw new Error("Invalid response: No `audio_url` found");
            }
        } catch (error) {
            console.error("❌ Upload failed:", error);
            setError("Something went wrong. Please check console for details.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <h1>Upload Your Slides</h1>
            <input type="file" accept=".pdf,.pptx" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Processing..." : "Upload & Generate Audio"}
            </button>

            {error && <p className="error">{error}</p>}
        </div>
    );
}
