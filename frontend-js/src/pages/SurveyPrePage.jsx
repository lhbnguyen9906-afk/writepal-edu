import { useState } from "react";
import { useNavigate } from "react-router-dom";

function SurveyPrePage() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const [level, setLevel] = useState("");
  const [pain, setPain] = useState("");
  const [preference, setPreference] = useState("");

  const handleSubmit = async () => {
    if (!name || !email || !level || !pain || !preference) {
      alert("Please fill all fields");
      return;
    }

    try {
      // 1. create user
      const userRes = await fetch("http://127.0.0.1:8000/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name,
          email
        })
      });

      const userData = await userRes.json();
      const userId = userData.user_id;

      localStorage.setItem("user_id", userId);

      // 2. submit survey
      await fetch("http://127.0.0.1:8000/survey/pre", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: userId,
          level: level,
          pain_points: pain,
          preference: preference
        })
      });

      // 3. go to chat
      navigate("/chat");

    } catch (err) {
      console.error(err);
      alert("Error connecting to server");
    }
  };

  return (
    <div style={{ padding: 40, maxWidth: 600 }}>
      <h2>🧠 Quick Setup</h2>

      {/* BASIC */}
      <h3>Basic Info</h3>

      <input
        placeholder="Your name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />

      <input
        placeholder="Your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ width: "100%", marginBottom: 20 }}
      />

      {/* LEVEL */}
      <label>English Level:</label>
      <select
        value={level}
        onChange={(e) => setLevel(e.target.value)}
        style={{ width: "100%", marginBottom: 20 }}
      >
        <option value="">Select...</option>
        <option value="Beginner">Beginner</option>
        <option value="Intermediate">Intermediate</option>
        <option value="Upper-intermediate">Upper-intermediate</option>
        <option value="Advanced">Advanced</option>
      </select>

      {/* PAIN POINT */}
      <label>Biggest difficulty when writing:</label>
      <select
        value={pain}
        onChange={(e) => setPain(e.target.value)}
        style={{ width: "100%", marginBottom: 20 }}
      >
        <option value="">Select...</option>
        <option value="start">Don't know how to start</option>
        <option value="structure">Don't understand structure</option>
        <option value="idea">Lack of ideas</option>
        <option value="grammar">Grammar mistakes</option>
      </select>

      {/* PREFERENCE */}
      <label>How do you want AI to help?</label>
      <select
        value={preference}
        onChange={(e) => setPreference(e.target.value)}
        style={{ width: "100%", marginBottom: 30 }}
      >
        <option value="">Select...</option>
        <option value="fix">Fix everything for me</option>
        <option value="guide">Show errors, I fix myself</option>
        <option value="hybrid">Combine both</option>
      </select>

      <button onClick={handleSubmit}>
        Continue to Chat →
      </button>
    </div>
  );
}

export default SurveyPrePage;