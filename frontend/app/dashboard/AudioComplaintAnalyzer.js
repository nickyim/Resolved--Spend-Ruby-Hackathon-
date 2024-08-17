'use client';

import { useState } from "react";
import axios from "axios";

// CSS
import styles from "./AudioComplaintAnalyzer.module.css";  // Make sure this file exists with the relevant styles

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

      const response = await axios.post(
        "http://127.0.0.1:5000/api/audioQuery",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Audio file submitted:", response.data);
    } catch (e) {
      console.log("ERROR: ", e);
    }
  };

  return (
    <div className={styles.AudioComplaintAnalyzer}>
      <div className={styles.AudioComplaintAnalyzer_Top}>
        <h2>Audio Complaint Analyzer</h2>
        <div className={styles.AudioComplaintAnalyzer_Form}>
          <input type="file" onChange={handleFileChange} className={styles.FileInput} />
          <button onClick={handleFileSubmit} className={styles.SubmitButton}>Submit File</button>
        </div>
      </div>
    </div>
  );
}