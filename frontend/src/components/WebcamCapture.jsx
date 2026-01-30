import React, { useRef, useState, useCallback } from 'react';
import Webcam from 'react-webcam';

const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "environment"
};

const WebcamCapture = ({ onCapture }) => {
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc);
    }, [webcamRef]);

    const retake = () => {
        setImgSrc(null);
    };

    const confirm = () => {
        if (imgSrc) {
            fetch(imgSrc)
                .then(res => res.blob())
                .then(blob => {
                    const file = new File([blob], "webcam_capture.jpg", { type: "image/jpeg" });
                    onCapture(file);
                });
        }
    };

    const handleUserMediaError = useCallback((error) => {
        console.error("Webcam error:", error);
        alert(`Camera failed: ${error.message || error}. \nNote: Browsers block camera access on non-secure (HTTP) connections except localhost. If on mobile, try enabling 'Insecure origins treated as secure' in chrome://flags.`);
    }, []);

    return (
        <div className="flex flex-col items-center w-full">
            {imgSrc ? (
                <div className="w-full max-w-lg p-4 bg-gray-800 rounded-lg border border-gray-700">
                    <img src={imgSrc} alt="Captured" className="rounded-lg shadow-lg w-full border border-gray-600" />
                    <div className="mt-4 flex justify-center space-x-4">
                        <button onClick={retake} className="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-full text-white font-medium transition-colors border border-gray-500">
                            Retake
                        </button>
                        <button onClick={confirm} className="px-6 py-2 bg-green-600 hover:bg-green-500 rounded-full text-white font-medium transition-colors shadow-lg shadow-green-900/50">
                            Analyze Photo
                        </button>
                    </div>
                </div>
            ) : (
                <div className="relative w-full max-w-lg bg-black rounded-lg overflow-hidden shadow-2xl border border-gray-700">
                    <Webcam
                        audio={false}
                        ref={webcamRef}
                        screenshotFormat="image/jpeg"
                        videoConstraints={videoConstraints}
                        className="w-full h-full object-cover"
                        onUserMediaError={handleUserMediaError}
                        onUserMedia={(stream) => console.log("Webcam started", stream)}
                    />
                    <div className="absolute bottom-6 left-0 right-0 flex justify-center">
                        <button
                            onClick={capture}
                            className="group relative flex items-center justify-center w-16 h-16 rounded-full border-4 border-white transition-all hover:bg-white/20 active:scale-95"
                            aria-label="Capture photo"
                        >
                            <div className="w-12 h-12 bg-white rounded-full group-active:scale-90 transition-transform"></div>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default WebcamCapture;
