//Components
'use client'; 
import { useState } from "react";  // Import useState
import ComplaintTab from './ComplaintTab'
import ViewPort from './ViewPort'

//CSS
import styles from './page.module.css'

export default function dashboard() {
    const [activeTab, setActiveTab] = useState("Text");
    return (
      <div className={styles.dashboard}>
        <ComplaintTab setActiveTab={setActiveTab} />
        <ViewPort />
      </div>
    );
}