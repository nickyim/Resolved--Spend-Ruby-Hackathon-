"use client";

import { useState, useRef } from "react";
import axios from "axios";

export default function ComplaintTab() {
  const [prompt, setPrompt] = useState("");
  const [audioFile, setAudioFile] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const [audioChunks, setAudioChunks] = useState([]);

  const handlePromptChange = (e) => {
    const { value } = e.target;
    setPrompt(value);
  };

  const handlePromptSubmit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/textQuery", {
        prompt: prompt,
      });
      console.log("TEST: ", response.data);
    } catch (e) {
      console.log("ERROR: ", e);
    }
  };

  const startRecording = () => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;
        mediaRecorder.start();
        setIsRecording(true);

        mediaRecorder.ondataavailable = (e) => {
          setAudioChunks((prev) => [...prev, e.data]);
        };

        mediaRecorder.onstop = () => {
          const blob = new Blob(audioChunks, { type: "audio/webm" });
          setAudioFile(blob);
          setAudioChunks([]);
          setIsRecording(false);
        };
      })
      .catch((err) => console.log("ERROR: ", err));
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const handleAudioSubmit = async () => {
    try {
      const formData = new FormData();
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" }); // Convert to audio/wav
      formData.append("audioFile", audioBlob);

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
    <div>
      <h2>Complaint Management</h2>
      <textarea value={prompt} onChange={handlePromptChange} />
      <button onClick={handlePromptSubmit}>Submit Prompt</button>
      <br />

      <div>
        <button onClick={isRecording ? stopRecording : startRecording}>
          {isRecording ? "Stop Recording" : "Start Recording"}
        </button>
        {audioFile && <button onClick={handleAudioSubmit}>Submit Audio</button>}
      </div>
    </div>
  );
}
