import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const AnomalyDistributionChart = ({ data }) => {
  return (
    <div className="my-8">
      <h3 className="text-xl font-bold mb-2">⚠️ Anomaly Distribution Across Sites</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="site_id" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="anomalies" fill="#f97316" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AnomalyDistributionChart;
