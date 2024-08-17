'use client'

import { useState } from 'react';

//CSS
import styles from './ComplaintTab.module.css'

export default function ComplaintTab() {
    const [tabs, setTabs] = useState(["Credit Card", "Debit Card"])
    const [active, setActive] = useState(0)

    return (
      <div className={styles.ComplaintTab}>
        <div className={styles.ComplaintTab_Header}>
            <h3>Dashboard</h3>
        </div>
        <div className={styles.ComplaintTab_Tabs}>
            {tabs.map((tab, idx) => (
                <button key={idx} className={idx === active ? styles.ComplaintTab_Tabs_Active : styles.ComplaintTab_Tabs_Inactive}>{tab}</button>
            ))}
        </div>
      </div>
    );
}