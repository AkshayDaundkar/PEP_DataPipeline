const ProcessedDataTable = ({ records }) => {
  if (!records || records.length === 0) {
    return <p className="text-gray-500">No processed data found.</p>;
  }

  return (
    <div className="overflow-x-auto mt-6">
      <table className="w-full border text-sm text-left text-gray-700 shadow-md rounded-md">
        <thead className="bg-gray-200 text-xs uppercase text-gray-700">
          <tr>
            <th className="px-4 py-3">Site</th>
            <th className="px-4 py-3">Timestamp</th>
            <th className="px-4 py-3">Generated (kWh)</th>
            <th className="px-4 py-3">Consumed (kWh)</th>
            <th className="px-4 py-3">Net (kWh)</th>
            <th className="px-4 py-3">Anomaly</th>
          </tr>
        </thead>
        <tbody>
          {records.map((rec, i) => (
            <tr
              key={i}
              className={`${
                rec.anomaly
                  ? "bg-red-100 font-semibold text-red-800"
                  : "bg-white"
              } border-b`}
            >
              <td className="px-4 py-2">{rec.site_id}</td>
              <td className="px-4 py-2">
                {new Date(rec.timestamp).toLocaleString()}
              </td>
              <td className="px-4 py-2">{rec.energy_generated_kwh}</td>
              <td className="px-4 py-2">{rec.energy_consumed_kwh}</td>
              <td className="px-4 py-2">{rec.net_energy_kwh}</td>
              <td className="px-4 py-2">{rec.anomaly ? "⚠️ Yes" : "✅ No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProcessedDataTable;
