'use client';

import { useState } from 'react';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa'; 
import { UserButton, useUser } from '@clerk/nextjs';
import styles from './ComplaintTab.module.css';

export default function ComplaintTab() {
    const [tabs, setTabs] = useState(["Credit Card", "Debit Card"]);
    const [active, setActive] = useState(0);
    const [collapsed, setCollapsed] = useState(false);
    const { user } = useUser();

    const toggleCollapse = () => {
        setCollapsed(!collapsed);
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
                        onClick={() => setActive(idx)} /* Make tabs clickable */
                    >
                        {tab}
                    </button>
                ))}
            </div>
        </div>
    );
}
