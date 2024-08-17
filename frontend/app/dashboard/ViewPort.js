"use client";

import { useState } from "react";
import axios from "axios";

export default function ComplaintTab() {
  const [prompt, setPrompt] = useState("");

  const handlePromptChange = (e) => {
    const { value } = e.target;
    setPrompt(value);
  };

  const handlePromptSubmit = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/prompt", {
        prompt: prompt,
      });
      console.log("TEST: ", response.data);
    } catch (e) {
      console.log("ERROR: ", e);
    }
  };

  return (
    <div>
      <h2>Complaint Management</h2>
      <textarea value={prompt} onChange={handlePromptChange} />
      <button onClick={handlePromptSubmit}>Submit</button>
    </div>
  );
}
