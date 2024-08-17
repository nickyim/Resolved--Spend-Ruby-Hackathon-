'use client'

import { useState } from 'react';
import axios from 'axios'

//CSS
import styles from './ViewPort.module.css'

export default function ViewPort() {
    const [prompt, setPrompt] = useState('')
    const [complaints, setComplaints] = useState([{id: 1, product: 'Credit Card', sub_product: 'Store credit card'}, {id: 2, product: 'Debit Card', sub_product: 'Store debit card'}])

    /*
        - Obejctive: Based on user input on prompt textarea, set state 'prompt' as current value
    */
    const handlePromptChange = (e) => {
        const {value} = e.target
        setPrompt(value)
    }

    /*
        - Obejctive: On user submission of prompt, send the prompt to server side endpoint: '/api/prompt'
    */
    const handlePromptSubmit = async () => {
        try {
            await axios.post('/api/prompt', {
                prompt: prompt
            })
            //Implement a .then(() => ) when server is capable of responding back
        } catch (e) {
            console.log(e)
        }
    }

    return (
      <div className={styles.ViewPort}>
        <div>
            <h2>Credit Card</h2>
            <div className={styles.ViewPort_Prompt}>
                <input type='text' value={prompt} onChange={handlePromptChange}/>
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
                    <p className={styles.ViewPort_List_Content_Sub_Product}>Sub-Product</p>
                </div>
                {complaints.map((complaint, idx) => (
                    <div key={idx} className={styles.ViewPort_List_Content_Tab + ' ' + styles.ViewPort_List_Content_Tab_Complaints}>
                        <p className={styles.ViewPort_List_Content_ID}>{complaint.id}</p>
                        <p className={styles.ViewPort_List_Content_Product}>{complaint.product}</p>
                        <p className={styles.ViewPort_List_Content_Sub_Product}>{complaint.sub_product}</p>
                    </div>
                ))}
            </div>
        </div>
      </div>
    );
}