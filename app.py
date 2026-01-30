from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from predict import predict_disease
from database import engine, get_db
import models
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kisan Drishti")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        print(f"DEBUG: temp_file_path = {temp_file_path}")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Make prediction
        result = predict_disease(temp_file_path)
        
        # Clean up
        os.remove(temp_file_path)
        
        if result:
            # Save to database
            db_prediction = models.Prediction(
                filename=file.filename,
                disease_class=result['class'],
                confidence=result['confidence']
            )
            db.add(db_prediction)
            db.commit()
            db.refresh(db_prediction)
            
            return result
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    predictions = db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).limit(10).all()
    # Format the data for the frontend
    import datetime
    formatted_history = []
    # IST Offset: UTC + 5:30
    ist_offset = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    
    for p in predictions:
        # p.timestamp is naive UTC. We make it aware, then convert to IST.
        ist_time = p.timestamp.replace(tzinfo=ist_offset)
        
        formatted_history.append({
            "disease": p.disease_class,
            "confidence": p.confidence,
            "date": ist_time.strftime("%d %b %Y, %I:%M %p") # e.g. 23 Dec 2025, 07:30 PM
        })
    return formatted_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
