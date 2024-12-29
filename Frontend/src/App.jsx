import React, { useState } from "react";
import axios from "axios";

function App() {
  const [videoUrl, setVideoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setAnswer(""); // Reset the answer field

    try {
      const response = await axios.post("http://127.0.0.1:5000/ask", {
        video_url: videoUrl,
        question: question,
      });
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Error processing your request. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>YouTube Transcript Q&A</h1>
      <div>
        <label>YouTube Video URL:</label>
        <input
          type="text"
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          style={{ width: "100%", padding: "8px", margin: "10px 0" }}
        />
      </div>
      <div>
        <label>Your Question:</label>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "100%", padding: "8px", margin: "10px 0" }}
        />
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Get Answer"}
      </button>
      <div style={{ marginTop: "20px" }}>
        <h3>Answer:</h3>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;
