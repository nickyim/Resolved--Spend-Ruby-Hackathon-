"use client";
import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Chart as ChartJS } from "chart.js/auto";
import { Doughnut } from "react-chartjs-2";
import { useUser } from "@clerk/nextjs";
import styles from "../../styles/ViewPort.module.css";
import { formatTextChunk } from "../utils/formatText";

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
  const [isFullTextVisible, setIsFullTextVisible] = useState(false);
  const [filter, setFilter] = useState("all");
  const [isAIOpen, setIsAIOpen] = useState(false);
  const [aiChatPrompt, setAiChatPrompt] = useState("");
  const [isAiThinking, setIsAiThinking] = useState(false);
  const [aiChatLog, setAiChatLog] = useState([]);
  const chatContainerRef = useRef(null);

  const toggleFullTextVisibility = () => {
    setIsFullTextVisible(!isFullTextVisible);
  };

  const toggleAIOpen = () => {
    setIsAIOpen(!isAIOpen);
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [aiChatLog]);

  useEffect(() => {
    const fetchData = async () => {
      if (!user || !user.id) return;

      try {
        setIsLoading(true);
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/api/getDashboard`,
          {
            headers: {
              Authorization: `Bearer ${user.id}`,
            },
          }
        );

        setInitialComplaints(response.data);
        setComplaints(response.data);
        let dataComplaints = 0;
        for (let i = 0; i < response.data.length; i++) {
          if (response.data[i].isComplaint) {
            dataComplaints++;
          }
        }

        setData([response.data.length - dataComplaints, dataComplaints]);

        // Automatically display the first complaint and highlight it
        if (response.data.length > 0) {
          let temp = response.data[0];
          let dateTemp = new Date(temp.created_at);
          let newDate =
            dateTemp.getMonth() +
            1 +
            "/" +
            dateTemp.getDate() +
            "/" +
            dateTemp.getFullYear();
          temp.created_at = newDate;
          setComplaint(temp);
          setSelectedComplaintIdx(0); // Highlight the first complaint
          // setData([response.data[0].isComplaint ? 1 : 0, response.data[0].isComplaint ? 0 : 1]);
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
    if (inputEntry) {
      setInitialComplaints((prev) => [...prev, inputEntry]);
      setComplaints((prev) => [...prev, inputEntry]);
    }
  }, [inputEntry]);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const handleSearchChange = (e) => {
    const { value } = e.target;
    setSearch(value);
  };

  const handleAIChatPromptChange = (e) => {
    const { value } = e.target;
    setAiChatPrompt(value);
  };

  const handleAIChatPromptSend = async () => {
    let temp = { content: aiChatPrompt, isUser: true };
    setAiChatLog((prev) => [...prev, temp]);
    setAiChatPrompt(""); // Clear the input field
    setIsAiThinking(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/smartSearch`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${user.id}`,
          },
          body: JSON.stringify({ query: aiChatPrompt }),
        }
      );

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = "";
      const processText = async ({ done, value }) => {
        if (done) {
          setIsAiThinking(false);
          // setAiChatLog((prev) => [...prev, { content: result, isUser: false }]);
          return;
        }
        const text = decoder.decode(value || new Int8Array(), { stream: true });

        const formattedText = formatTextChunk(text);

        result += formattedText;
        setAiChatLog((prev) => {
          const lastLog = prev[prev.length - 1];
          if (lastLog && !lastLog.isUser) {
            // Update the last AI message
            return [...prev.slice(0, -1), { content: result, isUser: false }];
          } else {
            // Add a new AI message
            return [...prev, { content: result, isUser: false }];
          }
        });
        reader.read().then(processText);
      };
      reader.read().then(processText);
    } catch (e) {
      console.error("Error sending AI chat prompt:", e);
      setAiChatLog((prev) => [
        ...prev,
        {
          content: "Sorry I didn't catch that . . . try again. :(",
          isUser: false,
        },
      ]);
      setIsAiThinking(false);
    }
  };

  const handleSearchSubmit = () => {
    let result = [];

    if (parseInt(search)) {
      for (let i = 0; i < initialComplaints.length && search.length > 0; i++) {
        if (
          initialComplaints[i] &&
          initialComplaints[i].id === Number.parseInt(search)
        ) {
          if (
            filter.toLowerCase() === "complaints" &&
            initialComplaints[i].isComplaint
          ) {
            result.push(initialComplaints[i]);
          } else if (
            filter.toLowerCase() === "non-complaints" &&
            !initialComplaints[i].isComplaint
          ) {
            result.push(initialComplaints[i]);
          } else {
            result.push(initialComplaints[i]);
          }
        }
      }
    } else {
      for (let i = 0; i < initialComplaints.length && search.length > 0; i++) {
        if (
          initialComplaints[i] &&
          ((initialComplaints[i].product &&
            initialComplaints[i].product.toLowerCase() ===
              search.toLowerCase()) ||
            (initialComplaints[i].subProduct &&
              initialComplaints[i].subProduct.toLowerCase() ===
                search.toLowerCase()) ||
            (initialComplaints[i].fileType &&
              initialComplaints[i].fileType.toLowerCase() ===
                search.toLowerCase()))
        ) {
          console.log(filter.toLowerCase());
          console.log(filter.toLowerCase() === "complaints");
          console.log(filter.toLowerCase() === "non-complaints");
          console.log(filter.toLowerCase() === "all");
          console.log("\n");
          if (
            filter.toLowerCase() === "complaints" &&
            initialComplaints[i].isComplaint
          ) {
            result.push(initialComplaints[i]);
          } else if (
            filter.toLowerCase() === "non-complaints" &&
            !initialComplaints[i].isComplaint
          ) {
            result.push(initialComplaints[i]);
          } else if (filter.toLowerCase() === "all") {
            result.push(initialComplaints[i]);
          }
        }
      }
    }

    if (result.length === 0) {
      setComplaints(initialComplaints);
    } else {
      setComplaints(result);
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
        `${process.env.NEXT_PUBLIC_API_URL}/api/audioQuery`,
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

    let temp = complaints[idx];
    let dateTemp = new Date(temp.created_at);
    let newDate =
      dateTemp.getMonth() +
      1 +
      "/" +
      dateTemp.getDate() +
      "/" +
      dateTemp.getFullYear();
    temp.created_at = newDate;
    setComplaint(temp);
  };

  if (isLoading) {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <div
            className={
              styles.ViewPort_Statement_IsLoading + " " + styles.IsLoading
            }
          ></div>
        </div>
        <div className={styles.ViewPort_Content}>
          <div className={styles.ViewPort_Top}>
            <div className={styles.ViewPort_Complaint}>
              <div className={styles.ViewPort_Complaint_Title}>
                <div
                  className={
                    styles.ViewPort_Statement_IsLoading + " " + styles.IsLoading
                  }
                ></div>
                <div
                  className={
                    styles.ViewPort_Statement_IsLoading + " " + styles.IsLoading
                  }
                ></div>
              </div>
              <div className={styles.ViewPort_Complaint_Content_Summary}>
                <div
                  className={
                    styles.ViewPort_Big_Statement_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
              </div>
            </div>
            <div className={styles.ViewPort_Chart}>
              <Doughnut
                data={{
                  labels: ["Non-Complaints", "Complaints"],
                  datasets: [
                    {
                      data: [50, 50],
                      backgroundColor: ["#d9d9d9", "#d9d9d9"],
                    },
                  ],
                }}
                options={{
                  plugins: {
                    legend: {
                      position: "bottom",
                    },
                  },
                }}
              />
            </div>
          </div>
          <div className={styles.ViewPort_Data}>
            <div className={styles.ViewPort_List}>
              <div className={styles.ViewPort_List_Title}>
                <h4>List of Entries</h4>
                <div className={styles.ViewPort_List_Search}>
                  <input
                    type="text"
                    value={search}
                    onChange={handleSearchChange}
                  />
                  <select value={filter} onChange={handleFilterChange}>
                    <option value="all">All</option>
                    <option value="complaints">Complaints</option>
                    <option value="non-complaints">Non-Complaints</option>
                  </select>
                  <button onClick={handleSearchSubmit}>Search</button>
                </div>
              </div>
              <div className={styles.ViewPort_List_Content}>
                <div className={styles.ViewPort_List_Content_Tab}>
                  <p className={styles.ViewPort_List_Content_ID}>ID</p>
                  <p className={styles.ViewPort_List_Content_Product}>
                    Product
                  </p>
                  <p className={styles.ViewPort_List_Content_Sub_Product}>
                    Sub-Product
                  </p>
                </div>
                <div
                  className={
                    styles.ViewPort_List_Complaint_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
                <div
                  className={
                    styles.ViewPort_List_Complaint_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
                <div
                  className={
                    styles.ViewPort_List_Complaint_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
                <div
                  className={
                    styles.ViewPort_List_Complaint_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
                <div
                  className={
                    styles.ViewPort_List_Complaint_IsLoading +
                    " " +
                    styles.IsLoading
                  }
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  } else if (hasError) {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <h2>Cannot Connect to Server</h2>
        </div>
      </div>
    );
  } else {
    return (
      <div className={styles.ViewPort}>
        <div className={styles.ViewPort_Header}>
          <h2>Dashboard</h2>
          <div>
            <button
              onClick={toggleAIOpen}
              className={
                isAIOpen ? styles.ViewPort_Header_AI_Prompt_Button_Closed : ""
              }
            >
              Smart Search the Complaints
            </button>
            <div
              className={`${styles.ViewPort_Header_AI_Prompt} ${
                isAIOpen
                  ? styles.ViewPort_Header_AI_Prompt_Open
                  : styles.ViewPort_Header_AI_Prompt_Closed
              } ${isAIOpen ? styles.Visible : ""}`}
            >
              <div className={styles.ViewPort_Header_AI_Prompt_Open_Header}>
                <h5>Complaint Assistance</h5>
                <button onClick={toggleAIOpen}>X</button>
              </div>

              <div
                className={styles.ViewPort_Header_AI_Prompt_Open_Output}
                ref={chatContainerRef}
              >
                {aiChatLog.map((chat, index) => (
                  <p
                    key={index}
                    className={
                      chat.isUser
                        ? styles.ViewPort_Header_AI_Prompt_Open_Output_User
                        : styles.ViewPort_Header_AI_Prompt_Open_Output_AI
                    }
                  >
                    {chat.isUser ? "You: " : "ResolveAI: "}
                    {chat.content}
                  </p>
                ))}
              </div>
              <div className={styles.ViewPort_Header_AI_Prompt_Open_Input}>
                <input
                  type="text"
                  value={aiChatPrompt}
                  onChange={handleAIChatPromptChange}
                />
                <button
                  onClick={handleAIChatPromptSend}
                  disabled={isAiThinking ? true : false}
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className={styles.ViewPort_Content}>
          <div className={styles.ViewPort_Top}>
            <div className={styles.ViewPort_Complaint}>
              <div className={styles.ViewPort_Complaint_Title}>
                <div className={styles.ViewPort_Complaint_Title_Content}>
                  <h4>
                    {complaint?.isComplaint && complaint?.product
                      ? complaint.product
                      : "N/A (Not a Complaint)"}
                  </h4>
                  <div
                    className={
                      complaint?.isComplaint
                        ? styles.ViewPort_List_Content_Sub_Is_Complaint
                        : styles.ViewPort_List_Content_Sub_Is_Not_Complaint
                    }
                  ></div>
                </div>
                <h4 className={styles.ViewPort_Complaint_Title_Subproduct}>
                  {complaint?.isComplaint && complaint?.subProduct
                    ? complaint.subProduct
                    : "N/A"}
                </h4>
              </div>
              <div className={styles.ViewPort_Complaint_Extra}>
                <button
                  className={styles.ViewPort_Complaint_ToggleButton}
                  onClick={toggleFullTextVisibility}
                >
                  {isFullTextVisible ? "Show Summary" : "Show Raw Context"}
                </button>
                <p className={styles.ViewPort_Complaint_Timestamp}>
                  {complaint?.created_at}
                </p>
              </div>
              <div className={styles.ViewPort_Complaint_Content_Summary}>
                {isFullTextVisible ? (
                  <p className={styles.ViewPort_Complaint_Summary}>
                    {complaint?.entryText}
                  </p>
                ) : (
                  <p className={styles.ViewPort_Complaint_Summary}>
                    {complaint?.summary}
                  </p>
                )}
              </div>
            </div>
            <div className={styles.ViewPort_Chart}>
              <Doughnut
                data={{
                  labels: ["Non-Complaints", "Complaints"],
                  datasets: [
                    {
                      data: data,
                      backgroundColor: ["#e9e3a6", "#e01e37"],
                    },
                  ],
                }}
                options={{
                  plugins: {
                    legend: {
                      position: "bottom",
                    },
                  },
                }}
              />
            </div>
          </div>
          <div className={styles.ViewPort_Data}>
            <div className={styles.ViewPort_List}>
              <div className={styles.ViewPort_List_Title}>
                <h4>List of Entries</h4>
                <div className={styles.ViewPort_List_Search}>
                  <input
                    type="text"
                    value={search}
                    onChange={handleSearchChange}
                  />
                  <select value={filter} onChange={handleFilterChange}>
                    <option value="all">All</option>
                    <option value="complaints">Complaints</option>
                    <option value="non-complaints">Non-Complaints</option>
                  </select>
                  <button onClick={handleSearchSubmit}>Search</button>
                </div>
              </div>
              <div className={styles.ViewPort_List_Content}>
                <div className={styles.ViewPort_List_Content_Tab}>
                  <p className={styles.ViewPort_List_Content_ID}>ID</p>
                  <p className={styles.ViewPort_List_Content_Product}>
                    Product
                  </p>
                  <p className={styles.ViewPort_List_Content_Sub_Product}>
                    Sub-Product
                  </p>
                  <p className={styles.ViewPort_List_Content_File_Type}>
                    File Type
                  </p>
                  <p
                    className={
                      styles.ViewPort_List_Content_Sub_Is_Complaint_Header
                    }
                  >
                    Complaint
                  </p>
                </div>
                {complaints.map((complaint, idx) => (
                  <div
                    key={idx}
                    className={
                      styles.ViewPort_List_Content_Tab +
                      " " +
                      styles.ViewPort_List_Content_Tab_Complaints +
                      (selectedComplaintIdx === idx
                        ? ` ${styles.SelectedComplaint}`
                        : "")
                    }
                    onClick={() => handleComplaintClick(idx)}
                  >
                    <p className={styles.ViewPort_List_Content_ID}>
                      {complaint.id}
                    </p>
                    <p className={styles.ViewPort_List_Content_Product}>
                      {complaint.isComplaint && complaint.product
                        ? complaint.product
                        : "N/A"}
                    </p>
                    <p className={styles.ViewPort_List_Content_Sub_Product}>
                      {complaint.isComplaint && complaint.subProduct
                        ? complaint.subProduct
                        : "N/A"}
                    </p>
                    <p className={styles.ViewPort_List_Content_File_Type}>
                      {complaint.fileType}
                    </p>
                    <div
                      className={
                        styles.ViewPort_List_Content_Sub_Is_Complaint_Content
                      }
                    >
                      <div
                        className={
                          complaint.isComplaint
                            ? styles.ViewPort_List_Content_Sub_Is_Complaint
                            : styles.ViewPort_List_Content_Sub_Is_Not_Complaint
                        }
                      ></div>
                    </div>
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
