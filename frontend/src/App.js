import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import Main from "./Main";
import Headlines from "./Headlines";
import Sites from "./Sites";
import EmotionSummary from "./EmotionSummary";
import ExportImport from "./ExportImport";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/main" element={<Main />} />
        <Route path="/headlines" element={<Headlines />} />
        <Route path="/sites" element={<Sites />} />
        <Route path="/emotion-summary" element={<EmotionSummary />} />
        <Route path="/export-import" element={<ExportImport />} />
      </Routes>
    </Router>
  );
}

export default App;
