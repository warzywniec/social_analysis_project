import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


export default function Headlines() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8000/headlines/", {
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

      <h2>Headlines</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.date} – {item.headline} – {item.emotion}
          </li>
        ))}
      </ul>
    </div>
  );
}
