import { useEffect, useState } from "react";
import EnergyComparisonChart from "./EnergyComparisonChart";
import AnomalyDistributionChart from "./AnomalyDistributionChart";
import EnergyTrendChart from "./EnergyTrendChart"; // Uncomment if you implement this chart

const Graphs = () => {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL + "/all-records")
      .then((res) => res.json())
      .then((data) => setRecords(data.records));
  }, []);

  const energyComparison = [];
  const anomalyMap = {};
  const energyTrend = [];

  const grouped = records.reduce((acc, rec) => {
    const site = rec.site_id;
    acc[site] = acc[site] || { site_id: site, generated: 0, consumed: 0 };
    acc[site].generated += rec.energy_generated_kwh;
    acc[site].consumed += rec.energy_consumed_kwh;
    return acc;
  }, {});
  Object.values(grouped).forEach((v) => energyComparison.push(v));

  records.forEach((rec) => {
    const site = rec.site_id;
    if (rec.anomaly) {
      anomalyMap[site] = (anomalyMap[site] || 0) + 1;
    }
    energyTrend.push({
      site_id: site,
      timestamp: new Date(rec.timestamp).toLocaleString(),
      net_energy_kwh: rec.net_energy_kwh,
    });
  });

  const anomalyData = Object.entries(anomalyMap).map(
    ([site_id, anomalies]) => ({
      site_id,
      anomalies,
    })
  );

  return (
    <div className="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow">
      <h2 className="text-3xl font-bold mb-6">📈 Energy Insights</h2>
      <EnergyComparisonChart data={energyComparison} />
      <AnomalyDistributionChart data={anomalyData} />
      <EnergyTrendChart data={energyTrend} />
    </div>
  );
};

export default Graphs;
