# 🍎 Fruit Disease Detection AI

## 📖 Overview

This project is a Deep Learning application designed to detect and classify diseases in fruits (e.g., [Apple, Banana, Orange]). By utilizing Convolutional Neural Networks (CNNs) and Computer Vision, this model analyzes images of fruit leaves or skin to identify potential infections, helping farmers and agriculturists take timely action.

## 🚀 Key Features

High Accuracy: Trained on a dataset of [Number] images.

Multi-Class Classification: Can detect [List diseases, e.g., Apple Scab, Black Rot] and healthy fruits.

Fast Processing: Optimized for quick inference on local machines.

User-Friendly: Simple script to test custom images.

## 🛠️ Tech Stack

Language: Python

Deep Learning: TensorFlow / Keras

Image Processing: OpenCV (cv2)

Data Handling: NumPy, Pandas

## 📂 Project Structure
```bash
./fruitdiseaseai/<br>
./│

./├── src/                # Source code for training and prediction

./├── model/              # Saved .keras/.h5 models (Use Git LFS)

./├── dataset/            # Raw images (Not included in repo)

./├── requirements.txt    # List of dependencies

./└── README.md           # Project documentation
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AryanJadile/fruitdiseaseai.git
```
```bash
cd fruitdiseaseai
```

### 2. Create a Virtual Environment (Recommended)

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 🧠 How to Run

Training the Model

To train the model from scratch using the dataset:
```bash
python src/train.py
```

### Testing / Prediction

To detect disease in a specific image:
```bash
python src/predict.py --image "path/to/fruit_image.jpg"
```

### 📊 Dataset
Dataset: [https://data.mendeley.com/datasets/3f83gxmv57/2](https://data.mendeley.com/datasets/3f83gxmv57/2)
You can also use your custom data to train the model.

### 🚧 Challenges & Future Improvements

Current Challenge: Handling large model files via Git LFS.

Future Goal: Deploy as a web app using Streamlit or Flask.

Future Goal: Add support for real-time detection via webcam.
.
