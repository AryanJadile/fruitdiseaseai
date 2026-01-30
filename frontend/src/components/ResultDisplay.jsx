import React from 'react';

const ResultDisplay = ({ image, result }) => {
    if (!image || !result) return null;

    const handleDownloadReport = () => {
        if (result.id) {
            window.open(`http://${window.location.hostname}:8000/report/${result.id}`, '_blank');
        } else {
            alert("Report not available for this prediction.");
        }
    };

    return (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg shadow-lg max-w-lg mx-auto">
            <h2 className="text-2xl font-bold mb-4 text-center text-green-400">Prediction Result</h2>

            <div className="mb-6">
                <img
                    src={URL.createObjectURL(image)}
                    alt="Uploaded Fruit"
                    className="w-full h-64 object-cover rounded-md border border-gray-600"
                />
            </div>

            <div className="space-y-4">
                <div className="flex justify-between items-center border-b border-gray-700 pb-2">
                    <span className="text-gray-300">Disease:</span>
                    <span className="text-xl font-semibold text-white">{result.class}</span>
                </div>

                <div>
                    <div className="flex justify-between mb-1">
                        <span className="text-gray-300">Confidence:</span>
                        <span className="text-green-300">{result.confidence.toFixed(2)}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2.5">
                        <div
                            className="bg-green-500 h-2.5 rounded-full"
                            style={{ width: `${result.confidence}%` }}
                        ></div>
                    </div>
                </div>

                {result.description && (
                    <div className="pt-2">
                        <h3 className="text-lg font-semibold text-gray-200 mb-1">Description</h3>
                        <p className="text-gray-400 text-sm">{result.description}</p>
                    </div>
                )}

                {result.remedies && result.remedies.length > 0 && (
                    <div className="pt-2">
                        <h3 className="text-lg font-semibold text-gray-200 mb-1">Recommended Treatments</h3>
                        <ul className="list-disc list-inside text-gray-400 text-sm space-y-1">
                            {result.remedies.map((remedy, index) => (
                                <li key={index}>{remedy}</li>
                            ))}
                        </ul>
                    </div>
                )}

                <div className="pt-4 text-center">
                    <button
                        onClick={handleDownloadReport}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded transition duration-200 shadow-md"
                    >
                        Download PDF Report
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;
