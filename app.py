from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os
from predict import predict_disease
from database import engine, get_db
import models
from sqlalchemy.orm import Session
from remedies import remedies
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

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
            
            # Enrich result with remedies and ID
            disease_class = result['class']
            treatment = remedies.get(disease_class, {
                "description": "No information available.",
                "remedies": []
            })
            
            response_data = {
                "id": db_prediction.id,
                "class": disease_class,
                "confidence": result['confidence'],
                "description": treatment["description"],
                "remedies": treatment["remedies"]
            }
            
            return response_data
        else:
            raise HTTPException(status_code=500, detail="Prediction failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{prediction_id}")
def generate_report(prediction_id: int, db: Session = Depends(get_db)):
    prediction = db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
        
    disease_class = prediction.disease_class
    treatment = remedies.get(disease_class, {
        "description": "No information available.",
        "remedies": ["Consult an expert."]
    })
    
    # Create PDF
    pdf_filename = f"report_{prediction_id}.pdf"
    pdf_path = os.path.join("temp_reports", pdf_filename)
    if not os.path.exists("temp_reports"):
        os.makedirs("temp_reports")
        
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Kisan Drishti Disease Report")
    
    # Date
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {prediction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Prediction
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 120, f"Detected Disease: {disease_class}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, f"Confidence: {prediction.confidence:.2f}%")
    
    # Description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 180, "Description:")
    c.setFont("Helvetica", 12)
    
    text_object = c.beginText(50, height - 200)
    text_object.setFont("Helvetica", 12)
    # Simple word wrap (very basic)
    words = treatment["description"].split()
    line = ""
    for word in words:
        if c.stringWidth(line + " " + word) < 500:
            line += " " + word
        else:
            text_object.textLine(line)
            line = word
    text_object.textLine(line)
    c.drawText(text_object)
    
    # Remedies
    y_pos = height - 250
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos, "Recommended Treatments:")
    
    y_pos -= 20
    c.setFont("Helvetica", 12)
    for remedy in treatment["remedies"]:
        c.drawString(70, y_pos, f"- {remedy}")
        y_pos -= 20
        
    c.save()
    
    return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)

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
        if p.timestamp.tzinfo is None:
             ist_time = p.timestamp.replace(tzinfo=datetime.timezone.utc).astimezone(ist_offset)
        else:
             ist_time = p.timestamp.astimezone(ist_offset)

        formatted_history.append({
            "disease": p.disease_class,
            "confidence": p.confidence,
            "date": ist_time.strftime("%d %b %Y, %I:%M %p") # e.g. 23 Dec 2025, 07:30 PM
        })
    return formatted_history

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
