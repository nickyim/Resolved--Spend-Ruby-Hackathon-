import React from "react";
import styles from "../styles/audioModal.module.css";

const AudioModal = ({ show, onClose, onSelect }) => {
  if (!show) {
    return null;
  }

  return (
    <div className={styles.modalOverlay}>
      <div className={styles.modalContent}>
        <h2>Select Transcription Service</h2>
        <button onClick={() => onSelect("assemblyAI")}>
          Transcribe with AssemblyAI
        </button>
        <button onClick={() => onSelect("googleCloud")}>
          Transcribe with Google Cloud
        </button>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default AudioModal;
