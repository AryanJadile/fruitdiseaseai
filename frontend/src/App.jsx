import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import WebcamCapture from './components/WebcamCapture';
import ResultDisplay from './components/ResultDisplay';
import PredictionHistory from './components/PredictionHistory';

function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('upload'); // 'upload' or 'camera'
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const response = await fetch(`http://${window.location.hostname}:8000/history`);
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (error) {
      console.error("Failed to fetch history:", error);
    }
  };

  React.useEffect(() => {
    fetchHistory();
  }, []);

  const handleUpload = async (file) => {
    setImage(file);
    setResult(null);
    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://${window.location.hostname}:8000/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const data = await response.json();
      setResult(data);
      // Refresh history from server
      fetchHistory();

    } catch (err) {
      console.error(err);
      setError('Failed to get prediction. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-extrabold tracking-tight text-green-500 sm:text-5xl">
            Kisan Drishti
          </h1>
          <p className="mt-4 text-xl text-gray-400">
            Upload an image of a fruit leaf or skin to detect diseases.
          </p>
        </header>


        <main>
          <div className="flex justify-center mb-8 bg-gray-800 p-1 rounded-lg inline-flex mx-auto w-max shadow-lg">
            <button
              onClick={() => setMode('upload')}
              className={`px-6 py-2 rounded-md font-medium transition-all duration-200 ${mode === 'upload'
                ? 'bg-green-600 text-white shadow-md'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
            >
              Upload File
            </button>
            <button
              onClick={() => setMode('camera')}
              className={`px-6 py-2 rounded-md font-medium transition-all duration-200 ${mode === 'camera'
                ? 'bg-green-600 text-white shadow-md'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
            >
              Use Camera
            </button>
          </div>

          <div className="transition-all duration-500 ease-in-out">
            {mode === 'upload' ? (
              <ImageUpload onUpload={handleUpload} />
            ) : (
              <WebcamCapture onCapture={handleUpload} />
            )}
          </div>

          {loading && (
            <div className="mt-8 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-500"></div>
              <p className="mt-2 text-gray-400">Analyzing image...</p>
            </div>
          )}

          {error && (
            <div className="mt-8 p-4 bg-red-900/50 border border-red-500 rounded-lg text-center text-red-200">
              {error}
            </div>
          )}

          <ResultDisplay image={image} result={result} />

          <PredictionHistory history={history} />
        </main>
      </div>
    </div >
  );
}

export default App;
