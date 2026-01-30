import React from 'react';

const PredictionHistory = ({ history }) => {
    if (!history || history.length === 0) {
        return null;
    }

    return (
        <div className="mt-12 max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold mb-4 text-gray-200 border-b border-gray-700 pb-2">Prediction History</h3>
            <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden border border-gray-700">
                <ul className="divide-y divide-gray-700">
                    {history.map((item, index) => (
                        <li key={index} className="p-4 hover:bg-gray-700 transition-colors flex justify-between items-center group">
                            <div>
                                <p className="font-semibold text-green-400 text-lg">{item.disease}</p>
                                <p className="text-sm text-gray-400">{item.date}</p>
                            </div>
                            <div className="text-right">
                                <span className="inline-block px-3 py-1 bg-gray-900 rounded-full text-sm font-medium text-blue-300 border border-blue-900/50">
                                    {item.confidence.toFixed(1)}% Confidence
                                </span>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default PredictionHistory;
