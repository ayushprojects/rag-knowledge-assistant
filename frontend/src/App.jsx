import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");

  async function handleUpload(e) {
    const file = e.target.files[0];
    e.target.value = "";
    if (!file) {
      return;
    }

    setUploading(true);
    setUploadStatus("Uploading " + file.name + "...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(API_URL + "/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        const reason =
          typeof data.detail === "string" ? data.detail : "Upload failed";
        throw new Error(reason);
      }

      setUploadStatus(
        "Done: " +
          data.filename +
          " (" +
          data.chunks_stored +
          " chunks stored)",
      );
    } catch (error) {
      setUploadStatus("Error: " + error.message);
    } finally {
      setUploading(false);
    }
  }

  async function handleSend() {
    const question = input.trim();
    if (question === "" || loading) {
      return;
    }

    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(API_URL + "/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question }),
      });

      if (!response.ok) {
        throw new Error("Server error " + response.status);
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.answer, sources: data.sources },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error: " + error.message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat">
      <h1>RAG Knowledge Assistant</h1>

      <div className="upload-row">
        <input
          type="file"
          accept=".pdf,.md"
          onChange={handleUpload}
          disabled={uploading}
        />
        {uploadStatus && <div className="status">{uploadStatus}</div>}
      </div>

      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={"message " + m.role}>
            {m.text}
            {m.sources && m.sources.length > 0 && (
              <div className="sources">
                Sources:{" "}
                {m.sources
                  .map((s) => s.source + " (page " + s.page + ")")
                  .join(", ")}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message bot">Thinking...</div>}
      </div>

      <div className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask a question..."
        />
        <button onClick={handleSend} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
