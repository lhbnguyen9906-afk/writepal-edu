import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: 60 }}>
      <h1>WritePal-Edu</h1>
      <button onClick={() => navigate("/survey-pre")}>
        Start Study
      </button>
    </div>
  );
}

export default LandingPage;