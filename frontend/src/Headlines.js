import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Headlines() {
  const [data, setData] = useState([]);
  const [skip, setSkip] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const navigate = useNavigate();

  const loadMore = () => {
    fetch(`http://localhost:8000/headlines/?skip=${skip}&limit=20`, {
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
      <h2>Headlines</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>
            {item.date} – {item.headline} – {item.emotion}
          </li>
        ))}
      </ul>
      {hasMore && <button onClick={loadMore}>Pokaż więcej</button>}
    </div>
  );
}
