import { Link, useLocation } from "react-router-dom";
import { FaRocket, FaFileAlt, FaChartBar, FaCogs } from "react-icons/fa";

const Sidebar = () => {
  const { pathname } = useLocation();

  const navItems = [
    { path: "/", name: "Simulate", icon: <FaRocket /> },
    { path: "/files", name: "Files", icon: <FaFileAlt /> },
    { path: "/processeddata", name: "Process Data", icon: <FaChartBar /> },
    { path: "/graphs", name: "Graphs", icon: <FaChartBar /> },
    { path: "/settings", name: "Settings", icon: <FaCogs /> },
  ];

  return (
    <div className="h-screen w-60 bg-white border-r shadow-md flex flex-col">
      <div className="text-2xl font-bold text-center py-6 border-b">
        ⚡ Dashboard
      </div>
      <nav className="flex-1 p-4 space-y-4">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            className={`flex items-center gap-3 p-3 rounded-md text-gray-700 hover:bg-blue-100 transition ${
              pathname === item.path ? "bg-blue-100 font-semibold" : ""
            }`}
          >
            {item.icon}
            {item.name}
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
