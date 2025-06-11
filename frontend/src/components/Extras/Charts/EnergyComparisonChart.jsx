import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const EnergyComparisonChart = ({ data }) => {
  return (
    <div className="my-8">
      <h3 className="text-xl font-bold mb-2">📊 Energy Generated vs Consumed (per Site)</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="site_id" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="generated" fill="#2563eb" />
          <Bar dataKey="consumed" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EnergyComparisonChart;
