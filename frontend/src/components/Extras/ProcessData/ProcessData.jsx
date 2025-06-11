import { useState } from "react";
import ProcessedDataTable from "./ProcessedDataTable";
const ProcessedData = () => {
  const [siteId, setSiteId] = useState("");
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchProcessedData = async () => {
    if (!siteId) return;
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/records?site_id=${siteId}`
      );
      const data = await res.json();
      setRecords(data.records || []);
    } catch (err) {
      console.error("Error fetching processed data:", err);
    }
    setLoading(false);
  };

  return (
    <div className="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">📊 View Processed Data</h2>

      <div className="flex items-center gap-4 mb-4">
        <input
          type="text"
          placeholder="Enter Site ID (e.g., site_alpha)"
          className="border border-gray-300 px-4 py-2 rounded w-full"
          value={siteId}
          onChange={(e) => setSiteId(e.target.value)}
        />
        <button
          onClick={fetchProcessedData}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Fetch
        </button>
      </div>

      {loading ? (
        <p className="text-sm text-gray-500">Loading...</p>
      ) : (
        <ProcessedDataTable records={records} />
      )}
    </div>
  );
};

export default ProcessedData;
