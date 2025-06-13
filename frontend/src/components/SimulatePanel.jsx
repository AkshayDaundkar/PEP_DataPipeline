import { useEffect, useState } from "react";

function SimulatePanel() {
  const [loading, setLoading] = useState(false);
  const [log, setLog] = useState("");
  const [file, setFile] = useState("");
  const [intervalId, setIntervalId] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const [fileList, setFileList] = useState(() => {
    const saved = localStorage.getItem("simulatedFiles");
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem("simulatedFiles", JSON.stringify(fileList));
  }, [fileList]);

  // Clear rogue intervals on page load
  useEffect(() => {
    if (window.__simulateInterval) {
      clearInterval(window.__simulateInterval);
      window.__simulateInterval = null;
      console.log("✅ Cleared leftover simulation interval on load");
    }
  }, []);

  const simulateData = async () => {
    setLoading(true);
    setLog("Simulating data and uploading file...");

    try {
      const res = await fetch(import.meta.env.VITE_API_URL + "/simulatedata", {
        method: "POST",
      });

      const data = await res.json();

      if (res.ok) {
        const newFile = {
          filename: data.filename,
          timestamp: new Date().toISOString(),
        };
        setFile(data.filename);
        setFileList((prev) => [newFile, ...prev]);
        setLog(`File "${data.filename}" uploaded to S3`);
      } else {
        setLog(`Error: ${data.detail || "Simulation failed"}`);
      }
    } catch (err) {
      setLog(`Network error: ${err.message}`);
    }

    setLoading(false);
  };

  const simulateContinuously = () => {
    if (intervalId || window.__simulateInterval) return;

    const maxRuns = 3;
    const intervalDuration = 2 * 60 * 1000; // 2 minutes
    let runs = 1;

    const now = Date.now();
    const lastStart = localStorage.getItem("last_simulation_start");
    if (lastStart && now - parseInt(lastStart) < 10 * 60 * 1000) {
      setLog("⚠️ Simulation recently ran. Try again after 10 mins.");
      return;
    }

    localStorage.setItem("last_simulation_start", now.toString());

    simulateData(); // First run
    setIsSimulating(true);

    const id = setInterval(() => {
      if (runs >= maxRuns) {
        clearInterval(id);
        window.__simulateInterval = null;
        setIntervalId(null);
        setIsSimulating(false);
        setLog("Stopped: Max 3 simulations completed.");
        return;
      }
      simulateData();
      runs++;
    }, intervalDuration);

    window.__simulateInterval = id;
    setIntervalId(id);
    setLog("Continuous simulation started: every 2 mins, max 5 runs.");

    // Auto stop after 10 minutes
    setTimeout(() => {
      clearInterval(id);
      window.__simulateInterval = null;
      setIntervalId(null);
      setIsSimulating(false);
      setLog("⏱️ Stopped: 10-minute limit reached.");
    }, 10 * 60 * 1000);
  };

  const stopSimulation = () => {
    if (intervalId || window.__simulateInterval) {
      clearInterval(intervalId || window.__simulateInterval);
      window.__simulateInterval = null;
      setIntervalId(null);
      setIsSimulating(false);
      setLog("Continuous simulation manually stopped.");
    }
  };

  return (
    <div className="bg-white text-black p-6 sm:p-8 rounded-2xl shadow-2xl w-full max-w-3xl mx-auto mt-10 border border-gray-200">
      <h2 className="text-2xl sm:text-3xl font-bold mb-6 text-blue-900 flex items-center gap-2">
        Simulate Data
      </h2>

      <div className="flex flex-wrap gap-4 mb-4">
        <button
          onClick={simulateData}
          disabled={loading || isSimulating}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
        >
          {loading ? "Simulating..." : "Simulate Once"}
        </button>

        {!isSimulating && (
          <button
            onClick={simulateContinuously}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition"
          >
            Start Continuous
          </button>
        )}

        {isSimulating && (
          <button
            onClick={stopSimulation}
            className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition"
          >
            Stop Simulation
          </button>
        )}
      </div>

      {file && (
        <p className="mt-2 text-green-700 font-medium text-lg">
          File Created: <span className="font-mono">{file}</span>
        </p>
      )}

      <pre className="mt-4 bg-gray-100 p-4 rounded-md text-sm text-gray-700 border border-gray-200 whitespace-pre-wrap break-words">
        {log}
      </pre>

      {fileList.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-2 text-gray-800">
            Simulation History
          </h3>
          <ul className="space-y-2 text-sm text-gray-800">
            {fileList.map((entry, i) => (
              <li key={i} className="font-mono">
                <span className="text-blue-700">{entry.filename}</span>{" "}
                <span className="text-gray-500 ml-2">
                  ({new Date(entry.timestamp).toLocaleString()})
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default SimulatePanel;
