//Components
'use client'; 
import { useState } from "react";  // Import useState
import ComplaintTab from './ComplaintTab'
import ViewPort from './ViewPort'

//CSS
import styles from './page.module.css'

export default function dashboard() {
    const [activeTab, setActiveTab] = useState("Text");
    const [newEntry, setNewEntry] = useState(null);

    const handleNewEntry = (entry) => {
      setNewEntry(entry)
    }

    return (
      <div className={styles.dashboard}>
        <ComplaintTab setActiveTab={setActiveTab} onValueChange={handleNewEntry} />
        <ViewPort inputEntry={newEntry} />
      </div>
    );
}