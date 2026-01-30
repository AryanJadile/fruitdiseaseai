import React from 'react';

const ResultDisplay = ({ image, result }) => {
    if (!image || !result) return null;

    return (
        <div className="mt-8 p-6 bg-gray-800 rounded-lg shadow-lg max-w-md mx-auto">
            <h2 className="text-2xl font-bold mb-4 text-center">Prediction Result</h2>

            <div className="mb-6">
                <img
                    src={URL.createObjectURL(image)}
                    alt="Uploaded Fruit"
                    className="w-full h-64 object-cover rounded-md"
                />
            </div>

            <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <span className="text-gray-300">Disease:</span>
                    <span className="text-xl font-semibold text-green-400">{result.class}</span>
                </div>

                <div>
                    <div className="flex justify-between mb-1">
                        <span className="text-gray-300">Confidence:</span>
                        <span className="text-white">{result.confidence.toFixed(2)}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2.5">
                        <div
                            className="bg-green-500 h-2.5 rounded-full"
                            style={{ width: `${result.confidence}%` }}
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;
