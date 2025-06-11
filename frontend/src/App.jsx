import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Extras/Sidebar";
import SimulatePanel from "./components/SimulatePanel";
import FileList from "./components/Extras/FIleViewer/FileList";
import ProcessedData from "./components/Extras/ProcessData/ProcessData";
import Graphs from "./components/Extras/Charts/Graphs";

function App() {
  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6 bg-gray-50 min-h-screen">
          <Routes>
            <Route path="/" element={<SimulatePanel />} />
            <Route path="/files" element={<FileList />} />
            <Route path="/processeddata" element={<ProcessedData />} />
            <Route path="/graphs" element={<Graphs />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
