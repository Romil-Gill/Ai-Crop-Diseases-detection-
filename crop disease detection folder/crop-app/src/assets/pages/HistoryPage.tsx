const HistoryPage = () => {
  const historyData = [
    { id: 1, date: "2024-03-20", crop: "Tomato", result: "Early Blight", confidence: "94%" },
    { id: 2, date: "2024-03-18", crop: "Potato", result: "Healthy", confidence: "98%" },
    { id: 3, date: "2024-03-15", crop: "Corn", result: "Common Rust", confidence: "89%" },
  ];

  return (
    <div className="container mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-8">Scan History</h1>
      <div className="bg-white rounded-xl shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b">
            <tr>
              <th className="px-6 py-4 font-semibold">Date</th>
              <th className="px-6 py-4 font-semibold">Crop</th>
              <th className="px-6 py-4 font-semibold">Diagnosis</th>
              <th className="px-6 py-4 font-semibold">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {historyData.map((item) => (
              <tr key={item.id} className="border-b hover:bg-slate-50">
                <td className="px-6 py-4">{item.date}</td>
                <td className="px-6 py-4">{item.crop}</td>
                <td className="px-6 py-4 font-medium text-emerald-700">{item.result}</td>
                <td className="px-6 py-4">{item.confidence}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoryPage;