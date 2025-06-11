import { useState } from "react";
import FileViewer from "./FileViewer";

const FileList = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);

  const fileList = JSON.parse(localStorage.getItem("simulatedFiles")) || [];

  const handleClick = async (filename) => {
    try {
      const res = await fetch(`http://localhost:8000/file/${filename}`);
      const data = await res.json();
      setSelectedFile(filename);
      setFileContent(data);
    } catch (err) {
      console.error("Error loading file:", err);
    }
  };

  return (
    <div className="p-4 bg-white rounded-xl shadow-md max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Uploaded Files</h2>
      {fileList.length === 0 ? (
        <p className="text-gray-500">No files yet.</p>
      ) : (
        <ul className="space-y-2">
          {fileList.map((entry, i) => (
            <li
              key={i}
              className={`cursor-pointer font-mono hover:text-blue-600 ${
                selectedFile === entry.filename
                  ? "font-bold text-blue-700"
                  : "text-gray-800"
              }`}
              onClick={() => handleClick(entry.filename)}
            >
              {entry.filename}
              <span className="ml-2 text-gray-500 text-xs">
                ({new Date(entry.timestamp).toLocaleString()})
              </span>
            </li>
          ))}
        </ul>
      )}

      <FileViewer fileData={fileContent} />
    </div>
  );
};

export default FileList;
