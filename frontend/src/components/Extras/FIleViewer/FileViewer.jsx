const FileViewer = ({ fileData }) => {
  if (!fileData) return null;

  return (
    <div className="mt-6 bg-gray-100 p-4 rounded-lg text-sm overflow-auto max-h-[500px] border border-gray-300">
      <h3 className="text-lg font-semibold mb-2 text-gray-800">File Content</h3>
      <pre className="whitespace-pre-wrap text-gray-700">
        {JSON.stringify(fileData, null, 2)}
      </pre>
    </div>
  );
};

export default FileViewer;
