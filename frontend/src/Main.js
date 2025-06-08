import { useNavigate } from "react-router-dom";

export default function Main() {
  const navigate = useNavigate();

  return (
    <div>
      <h2>Witaj w systemie</h2>
      <button onClick={() => navigate("/headlines")}>Headlines</button>
      <button onClick={() => navigate("/sites")}>Sites</button>
      <button onClick={() => navigate("/emotion-summary")}>Emotion Summary</button>
    </div>
  );
}
