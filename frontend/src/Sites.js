import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Sites() {
  const [data, setData] = useState([]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const navigate = useNavigate();

  const loadMore = () => {
    fetch(`http://localhost:8000/sites/?skip=${skip}&limit=20`, {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then((newData) => {
        setData((prev) => [...prev, ...newData]);
        setSkip((prev) => prev + 20);
        if (newData.length < 20) setHasMore(false);
      });
  };

  useEffect(() => {
    loadMore();
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

      {hasMore && (
        <div style={{ textAlign: "center", marginTop: "1rem" }}>
          <button onClick={loadMore}>Pokaż więcej</button>
        </div>
      )}
    </div>
  );
}
