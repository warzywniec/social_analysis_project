import { useNavigate } from "react-router-dom";

export default function ExportImport() {
  const navigate = useNavigate();

  const handleAction = async (endpoint) => {
    const response = await fetch(`http://localhost:8000/${endpoint}`, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("token"),
      },
    });

    const data = await response.json();
    alert(data.message || "Operacja zakończona");
  };

  return (
    <div>
      <div style={{ position: "absolute", top: 10, right: 10 }}>
        <button onClick={() => navigate("/main")}>Powrót do strony głównej</button>
      </div>

      <h2>Import / Eksport danych</h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "1rem", maxWidth: "200px" }}>
        <button onClick={() => handleAction("export/json")}>Eksportuj JSON</button>
        <button onClick={() => handleAction("export/xml")}>Eksportuj XML</button>
        <button onClick={() => handleAction("import/json")}>Importuj JSON</button>
        <button onClick={() => handleAction("import/xml")}>Importuj XML</button>
      </div>
    </div>
  );
}
