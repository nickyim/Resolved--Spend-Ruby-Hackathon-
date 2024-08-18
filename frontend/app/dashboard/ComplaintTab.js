'use client';

import { useState } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'; 
import { UserButton, useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';  // Import useRouter for navigation
import styles from './ComplaintTab.module.css';

export default function ComplaintTab() {
    const [viewTabs, setViewTabs] = useState(["Dashboard", "Settings"]);
    const [tabs, setTabs] = useState(["Text", "Audio"]);
    const [viewActive, setViewActive] = useState(0);
    const [active, setActive] = useState(0);
    const [collapsed, setCollapsed] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const { user } = useUser();
    const router = useRouter();  // Initialize useRouter

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
    };

    const handleFileSubmit = async () => {
        if (!selectedFile) return;
    
        try {
          const formData = new FormData();
          formData.append("audioFile", selectedFile);
    
          const response = await fetch("http://127.0.0.1:5000/api/audioQuery", {
            method: "POST",
            body: formData,
          });
    
          const result = await response.json();
          console.log("Audio file submitted:", result);
        } catch (e) {
          console.log("ERROR: ", e);
        }
    };

    const toggleCollapse = () => {
        setCollapsed(!collapsed);
    };

    // Function to handle tab clicks and navigation
    const handleViewTabClick = (idx) => {
        setViewActive(idx)
    };
    
    // Function to handle tab clicks and navigation
    const handleTabClick = (tab) => {
        if (tab === "Text") {
            router.push('/dashboard');  // Go to main dashboard page
        } else if (tab === "Audio") {
            router.push('/dashboard/audio');  // Navigate to audio handling page
        }
    };

    return (
        <div className={`${styles.ComplaintTab} ${collapsed ? styles.Collapsed : ''}`}>
            <div className={styles.ComplaintTab_Header}>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    {!collapsed && <UserButton />}
                    {!collapsed && (
                        <div style={{ paddingLeft: '1vw' }}>
                            <h3>{user?.fullName || user?.firstName}</h3>
                            <p>{user?.emailAddresses[0].emailAddress}</p>
                        </div>
                    )}
                </div>
                <div className={styles.CollapseButton} onClick={toggleCollapse}>
                    {collapsed ? <FaChevronRight /> : <FaChevronLeft />}
                </div>
            </div>
            <div className={`${styles.ComplaintTab_Tabs} ${collapsed ? styles.Hidden : ''}`}>
                <div className={styles.ComplaintTab_Tabs_ViewTabs}>
                    {viewTabs.map((tab, idx) => (
                        <button 
                            key={idx} 
                            className={idx === viewActive ? styles.ComplaintTab_Tabs_Active : styles.ComplaintTab_Tabs_Inactive}
                            onClick={() => handleViewTabClick(idx)}  // Handle tab click
                        >
                            {tab}
                        </button>
                    ))}
                </div>
                <div className={styles.ComplaintTab_Tabs_InputTabs}>
                    {tabs.map((tab, idx) => (
                        <button 
                            key={idx} 
                            className={idx === active ? styles.Input_Tabs_Active : styles.Input_Tabs_Inactive}
                            onClick={() => handleTabClick(tab)}  // Handle tab click
                        >
                            {tab}
                        </button>
                    ))}
                    <div className={styles.ComplaintTab_Tabs_File}>
                        <label for="file-upload">Upload</label>
                        <input id="file-upload" type="file" onChange={handleFileChange}/>
                        <button className={styles.ComplaintTab_Tabs_Submit} onClick={handleFileSubmit}>Submit</button>
                    </div>
                </div>
            </div>
        </div>
    );
}