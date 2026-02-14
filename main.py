from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('model.joblib')
tfidf = joblib.load('tfidf.joblib')

class NewsRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(request: NewsRequest):
    vectorized_text = tfidf.transform([request.text])
    prediction = model.predict(vectorized_text)
    return {"prediction": prediction[0]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)