document.getElementById('file-upload').addEventListener('change', async function(event) {
    const file = event.target.files[0];  // Get the file
    if (!file) return;  // If no file is selected, return

    // Create a new FormData object to send the file
    const formData = new FormData();
    formData.append("file", file);

    try {
        // Send a POST request to the backend to upload the file
        const response = await fetch('http://127.0.0.1:8000/upload', {  // Update with your backend URL
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Assuming the backend returns an audio URL in the response
            const result = await response.json();
            const audioUrl = result.audio_url; // Backend should return the audio URL

            // Redirect to a new page to play the generated audio
            window.location.href = `audio.html?audio_url=${encodeURIComponent(audioUrl)}`;
        } else {
            alert('File upload failed.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the file.');
    }
});
