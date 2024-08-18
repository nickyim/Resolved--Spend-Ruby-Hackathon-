"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import { Chart as ChartJS } from 'chart.js/auto';
import { Doughnut } from "react-chartjs-2";
import { useUser } from '@clerk/nextjs';
import styles from "./ViewPort.module.css";

export default function ViewPort({ inputEntry }) {
  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [search, setSearch] = useState("");
  const { user } = useUser(); 
  const [complaint, setComplaint] = useState(null);
  const [initialComplaints, setInitialComplaints] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [data, setData] = useState([]);
  const [selectedComplaintIdx, setSelectedComplaintIdx] = useState(0);


  useEffect(() => {
    const fetchData = async () => {
      if (!user || !user.id) return;
  
      try {
        setIsLoading(true);
        const response = await axios.get('http://127.0.0.1:5000/api/getDashboard', {
          headers: {
            Authorization: `Bearer ${user.id}`,
          },
        });
  
        console.log('Inside async');
        console.log(response.data);
        setInitialComplaints(response.data);
        setComplaints(response.data);
  
        // Automatically display the first complaint and highlight it
        if (response.data.length > 0) {
          setComplaint(response.data[0]);
          setSelectedComplaintIdx(0); // Highlight the first complaint
          setData([response.data[0].isComplaint ? 1 : 0, response.data[0].isComplaint ? 0 : 1]);
        }
      } catch (e) {
        setHasError(true);
        console.error("Error fetching dashboard data:", e);
      } finally {
        setIsLoading(false);
      }
    };
  
    fetchData();
  }, [user]);

  useEffect(() => {
    if(inputEntry) {
      setInitialComplaints((prev) => [
        ...prev,
        inputEntry
      ])
      setComplaints((prev) => [
        ...prev,
        inputEntry
      ])
    }
  }, [inputEntry])
  
  const handleSearchChange = (e) => {
    const { value } = e.target;
    setSearch(value);
  };

  const handleSearchSubmit = () => {
    let result = []
    if(parseInt(search)) {
      for(let i = 0; i < initialComplaints.length && search.length > 0; i++) {
        if(initialComplaints[i].id === Number.parseInt(search)) {
          result.push(initialComplaints[i])
        }
      }  
    } else {
      console.log(initialComplaints[0].product.toLowerCase())
      console.log(initialComplaints[0].subProduct.toLowerCase())
      for(let i = 0; i < initialComplaints.length && search.length > 0; i++) {
        if(initialComplaints[i].product.toLowerCase() === search.toLowerCase() || initialComplaints[i].subProduct.toLowerCase() === search.toLowerCase()) {
          result.push(initialComplaints[i])
        }
      }
    }

    if(result.length === 0) {
      setComplaints(initialComplaints)  
    } else {
      setComplaints(result)
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileSubmit = async () => {
    if (!selectedFile) return;

    try {
      const formData = new FormData();
      formData.append("audioFile", selectedFile);

      console.log("Selected file:", selectedFile);
      console.log("File type:", selectedFile.type);

      const response = await axios.post(
        "http://127.0.0.1:5000/api/audioQuery",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Audio file submitted:", response.data);
    } catch (e) {
      console.log("ERROR: ", e);
    }
  };

  const handleComplaintClick = (idx) => {
    setSelectedComplaintIdx(idx);
    setComplaint(complaints[idx]);
    setData([complaints[idx].isComplaint ? 1 : 0, complaints[idx].isComplaint ? 0 : 1]);
  };
  
  if (isLoading) {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <div className={styles.ViewPort_Statement_IsLoading + ' ' + styles.IsLoading}></div>
        </div>
        <div className={styles.ViewPort_Content}>
          <div className={styles.ViewPort_Top}>
            <div className={styles.ViewPort_Complaint}>
              <div className={styles.ViewPort_Complaint_Title}>
                <div className={styles.ViewPort_Statement_IsLoading + ' ' + styles.IsLoading}></div>
                <div className={styles.ViewPort_Statement_IsLoading + ' ' + styles.IsLoading}></div>
              </div>
              <div className={styles.ViewPort_Complaint_Content_Summary}>
                <div className={styles.ViewPort_Big_Statement_IsLoading + ' ' + styles.IsLoading}></div>
              </div>
            </div>
            <div className={styles.ViewPort_Chart}>
              <Doughnut
                data={{
                  labels: ["Non-Complaints", "Complaints"],
                  datasets: [
                    {
                      data: [50,50],
                      backgroundColor: ["#d9d9d9", "#d9d9d9"],
                    },
                  ],
                }}
                options={{
                  plugins: {
                    legend: {
                      position: 'bottom'
                    }
                  }
                }}
              />
            </div>
          </div>
          <div className={styles.ViewPort_Data}>
            <div className={styles.ViewPort_List}>
              <div className={styles.ViewPort_List_Title}>
                <h4>List of Complaints</h4>
                <div className={styles.ViewPort_List_Search}>
                  <input type="text" value={search} onChange={handleSearchChange} />
                  <button onClick={handleSearchSubmit} >Submit</button>
                </div>
              </div>
              <div className={styles.ViewPort_List_Content}>
                <div className={styles.ViewPort_List_Content_Tab}>
                  <p className={styles.ViewPort_List_Content_ID}>ID</p>
                  <p className={styles.ViewPort_List_Content_Product}>Product</p>
                  <p className={styles.ViewPort_List_Content_Sub_Product}>
                    Sub-Product
                  </p>
                </div>
                <div className={styles.ViewPort_List_Complaint_IsLoading + ' ' + styles.IsLoading}></div>
                <div className={styles.ViewPort_List_Complaint_IsLoading + ' ' + styles.IsLoading}></div>
                <div className={styles.ViewPort_List_Complaint_IsLoading + ' ' + styles.IsLoading}></div>
                <div className={styles.ViewPort_List_Complaint_IsLoading + ' ' + styles.IsLoading}></div>
                <div className={styles.ViewPort_List_Complaint_IsLoading + ' ' + styles.IsLoading}></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  } else if (hasError) {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <h2>Cannot Connect to Server</h2>
        </div>
      </div>
    )
  } else {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <h2>Dashboard</h2>
        </div>
        <div className={styles.ViewPort_Content}>
          <div className={styles.ViewPort_Top}>
            <div className={styles.ViewPort_Complaint}>
              <div className={styles.ViewPort_Complaint_Title}>
                <h4>{complaint?.product}</h4>
                <h4 className={styles.ViewPort_Complaint_Title_Subproduct}>{complaint?.subProduct}</h4>
              </div>
              <div className={styles.ViewPort_Complaint_Content_Summary}>
                <p className={styles.ViewPort_Complaint_Summary}>{complaint?.summary}</p>
              </div>
            </div>
            <div className={styles.ViewPort_Chart}>
              <Doughnut
                data={{
                  labels: ["Non-Complaints", "Complaints"],
                  datasets: [
                    {
                      data: data,
                      backgroundColor: ["#8cbdac", "#e9e3a6"],
                    },
                  ],
                }}
                options={{
                  plugins: {
                    legend: {
                      position: 'bottom'
                    }
                  }
                }}
              />
            </div>
          </div>
          <div className={styles.ViewPort_Data}>
            <div className={styles.ViewPort_List}>
              <div className={styles.ViewPort_List_Title}>
                <h4>List of Complaints</h4>
                <div className={styles.ViewPort_List_Search}>
                  <input type="text" value={search} onChange={handleSearchChange} />
                  <button onClick={handleSearchSubmit}>Submit</button>
                </div>
              </div>
              <div className={styles.ViewPort_List_Content}>
                <div className={styles.ViewPort_List_Content_Tab}>
                  <p className={styles.ViewPort_List_Content_ID}>ID</p>
                  <p className={styles.ViewPort_List_Content_Product}>Product</p>
                  <p className={styles.ViewPort_List_Content_Sub_Product}>
                    Sub-Product
                  </p>
                </div>
                {complaints.map((complaint, idx) => (
                  <div
                    key={idx}
                    className={
                      styles.ViewPort_List_Content_Tab +
                      " " +
                      styles.ViewPort_List_Content_Tab_Complaints +
                      (selectedComplaintIdx === idx ? ` ${styles.SelectedComplaint}` : "")
                    }
                    onClick={() => handleComplaintClick(idx)} // Handle click to select complaint
                  >
                    <p className={styles.ViewPort_List_Content_ID}>{complaint.id}</p>
                    <p className={styles.ViewPort_List_Content_Product}>
                      {complaint.product}
                    </p>
                    <p className={styles.ViewPort_List_Content_Sub_Product}>
                      {complaint.subProduct}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
