'use client';

import { useState } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'; 
import { UserButton, useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';  // Import useRouter for navigation
import styles from './ComplaintTab.module.css';

export default function ComplaintTab() {
    const [tabs, setTabs] = useState(["Text", "Audio"]);
    const [active, setActive] = useState(0);
    const [collapsed, setCollapsed] = useState(false);
    const { user } = useUser();
    const router = useRouter();  // Initialize useRouter

    const toggleCollapse = () => {
        setCollapsed(!collapsed);
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
                {tabs.map((tab, idx) => (
                    <button 
                        key={idx} 
                        className={idx === active ? styles.ComplaintTab_Tabs_Active : styles.ComplaintTab_Tabs_Inactive}
                        onClick={() => handleTabClick(tab)}  // Handle tab click
                    >
                        {tab}
                    </button>
                ))}
            </div>
        </div>
    );
}