import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

const ImageUpload = ({ onUpload }) => {
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0]);
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.jpg', '.png']
        },
        multiple: false
    });

    return (
        <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-10 text-center cursor-pointer transition-colors duration-300 ${isDragActive ? 'border-green-500 bg-gray-800' : 'border-gray-600 hover:border-gray-400'
                }`}
        >
            <input {...getInputProps()} />
            {isDragActive ? (
                <p className="text-green-400">Drop the image here...</p>
            ) : (
                <div>
                    <p className="text-lg mb-2">Drag & drop a fruit image here, or click to select</p>
                    <p className="text-sm text-gray-400">Supports JPG, JPEG, PNG</p>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
