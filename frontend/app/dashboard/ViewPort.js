"use client";

import { useState } from "react";
import axios from "axios";

//CSS
import styles from "./ViewPort.module.css";

export default function ViewPort() {
  const [prompt, setPrompt] = useState("");
  const [complaints, setComplaints] = useState([
    { id: 1, product: "Credit Card", sub_product: "Store credit card" },
    { id: 2, product: "Debit Card", sub_product: "Store debit card" },
  ]);
  const [selectedFile, setSelectedFile] = useState(null);

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

  const handlePromptChange = (e) => {
    const { value } = e.target;
    setPrompt(value);
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileSubmit = async () => {
    if (!selectedFile) return;

    try {
      const formData = new FormData();
      formData.append("audioFile", selectedFile);

      // Log file details for debugging
      console.log("Selected file:", selectedFile);
      console.log("File type:", selectedFile.type);

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
    <div className={styles.ViewPort}>
      <div>
        <h2>Credit Card</h2>
        <div className={styles.ViewPort_Prompt}>
          <input type="text" value={prompt} onChange={handlePromptChange} />
          <button onClick={handlePromptSubmit}>Submit</button>
        </div>
      </div>
      <div className={styles.ViewPort_List}>
        <div className={styles.ViewPort_List_Title}>
          <h3>List of Complaints</h3>
        </div>
        <div className={styles.ViewPort_List_Content}>
          <div className={styles.ViewPort_List_Content_Tab}>
            <p className={styles.ViewPort_List_Content_ID}>ID</p>
            <p className={styles.ViewPort_List_Content_Product}>Product</p>
            <p className={styles.ViewPort_List_Content_Sub_Product}>
              Sub-Product
            </p>
          </div>
          {complaints.map((complaint, idx) => (
            <div
              key={idx}
              className={
                styles.ViewPort_List_Content_Tab +
                " " +
                styles.ViewPort_List_Content_Tab_Complaints
              }
            >
              <p className={styles.ViewPort_List_Content_ID}>{complaint.id}</p>
              <p className={styles.ViewPort_List_Content_Product}>
                {complaint.product}
              </p>
              <p className={styles.ViewPort_List_Content_Sub_Product}>
                {complaint.sub_product}
              </p>
            </div>
          ))}
        </div>
      </div>
      <div>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleFileSubmit}>Submit File</button>
      </div>
    </div>
  );
}
