import styles from "./messageList.module.css";
import React, {useState} from "react";

const MessageList = () => {
    const [userMessage, setUserMessage] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!userMessage.trim()) return; // Prevent sending empty messages
        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ prompt: userMessage, }),
            });

            if (!response.ok) {
                throw new Error("Fail;ed to get response from the server");
            }

            const data = await response.json();
            setChatHistory((prev) => [
            ...prev, 
            { sender: "user", message: userMessage }, 
            { sender: "bot", message: data.response },
            ]);

            setUserMessage(""); // Clear the input field after sending the message

        } catch (error) {
            console.error("Error:", error);
            alert("Failed to send message. Please try again.");
        } finally {
            setLoading(false);
        }

    }


  return (
    <div className={styles.container}>
        <h1 className={styles.header}>Chat with GTP</h1>
        <div className={styles.chatBox}>
            {chatHistory.map((chat, index) => (
                <div 
                    key={index}
                    className={`${styles.message} ${chat.sender == "user" ? styles.userMessage : styles.botMessage}`}
                >
                    {chat.message}
                </div>
            ))}
        </div>
        <div className={styles.inputContainer}>
            <input 
                type="text" 
                className={styles.input} 
                placeholder="Type a message..." 
                value = {userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                disabled = {loading}
            />
            <button onClick={sendMessage} className={styles.button} disabled={loading}>
                { loading ? "Sending..." : "Send"}
            </button>
        </div>
    </div>
  );
}

export default MessageList