'use client'

import { useState } from 'react';
import axios from 'axios'

export default function ComplaintTab() {
    const [prompt, setPrompt] = useState('')

    const handlePromptChange = (e) => {
        const {value} = e.target
        setPrompt(value)
    }

    const handlePromptSubmit = async () => {
        try {
            await axios.post('http://localhost:3000/dashboard', {
                prompt: prompt
            })
        } catch (e) {
            console.log(e)
        }
    }

    return (
      <div>
        <h2>Complaint Management</h2>
        <textarea value={prompt} onChange={handlePromptChange}/>
        <button onClick={handlePromptSubmit}>Submit</button>
      </div>
    );
}