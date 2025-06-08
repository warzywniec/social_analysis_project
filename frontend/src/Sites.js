import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Sites() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8000/sites/", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then(setData);
  }, []);

  return (
    <div>
        <div style={{ position: "absolute", top: 10, right: 10 }}>
  <button onClick={() => navigate("/main")}>Powrót do strony głównej</button>
</div>

      <h2>Sites</h2>
      <ul>
        {data.map((site, index) => (
          <li key={index}>
            {site.date} – {site.name} – {site.category}
          </li>
        ))}
      </ul>
    </div>
  );
}
