"use client";

import { useState } from "react";

export default function AudioComplaintAnalyzer() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileSubmit = async () => {
    if (!selectedFile) return;

    try {
      const formData = new FormData();
      formData.append("audioFile", selectedFile);

      const response = await fetch(
        "http://127.0.0.1:5000/api/googleAudioQuery",
        {
          method: "POST",
          body: formData,
        }
      );

      const result = await response.json();
      console.log("Audio file submitted:", result);
    } catch (e) {
      console.log("ERROR: ", e);
    }
  };

  return (
    <div>
      <h1>Audio Complaint Analyzer</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileSubmit}>Submit File</button>
    </div>
  );
}
