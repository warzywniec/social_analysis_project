import { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function EmotionSummary() {
  const [filters, setFilters] = useState({
    year: "",
    category: "",
    emotion: "",
  });
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const fetchSummary = async () => {
    const params = new URLSearchParams();
    if (filters.year) params.append("year", filters.year);
    if (filters.category) params.append("category", filters.category);
    if (filters.emotion) params.append("emotion", filters.emotion);

    const response = await fetch(
      `http://localhost:8000/emotion-summary/?${params.toString()}`,
      {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("token"),
        },
      }
    );

    const data = await response.json();
    setResults(data);
  };

  return (
    <div>
        <div style={{ position: "absolute", top: 10, right: 10 }}>
  <button onClick={() => navigate("/main")}>Powrót do strony głównej</button>
</div>

      <h2>Emotion Summary</h2>
      <input
        name="year"
        placeholder="Year"
        value={filters.year}
        onChange={handleChange}
      />
      <input
        name="category"
        placeholder="Category"
        value={filters.category}
        onChange={handleChange}
      />
      <input
        name="emotion"
        placeholder="Emotion"
        value={filters.emotion}
        onChange={handleChange}
      />
      <button onClick={fetchSummary}>Wyświetl rezultaty</button>

      <ul>
        {results.map((row, index) => (
          <li key={index}>
            {row.year} – {row.category} – {row.emotion} – {row.count}
          </li>
        ))}
      </ul>
    </div>
  );
}
