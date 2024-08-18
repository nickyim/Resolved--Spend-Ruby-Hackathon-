import React from "react";
import styles from "../styles/audioModal.module.css";

const AudioModal = ({ show, onClose, onSelect }) => {
  if (!show) {
    return null;
  }

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <div className={styles.modalContent_Header}>
          <h4>Select Transcription Service</h4>
          <button onClick={onClose}>X</button>
        </div>
        <div className={styles.modalContent_Content}>
          <button className={styles.modalContent_Content_AssemblyAI} onClick={() => onSelect("assemblyAI") }>
            AssemblyAI
          </button>
          <button className={styles.modalContent_Content_GoogleCloud} onClick={() => onSelect("googleCloud")}>
            Google Cloud
          </button>
        </div>
      </div>
    </div>
  );
};

export default AudioModal;
