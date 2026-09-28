from fastapi import FastAPI, UploadFile, File, HTTPException
import json
import csv
from io import StringIO
from cleaner import EnterpriseDataCleaner

app = FastAPI(title="AI Data Cleaner Micro-SaaS Engine", version="2.0")

@app.post("/api/v1/clean")
async def clean_dataset_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.json', '.jsonl')):
        raise HTTPException(status_code=400, detail="نوع الملف غير مدعوم. استخدم CSV أو JSON")
    
    content = (await file.read()).decode("utf-8")
    raw_data = []

    if file.filename.endswith('.csv'):
        reader = csv.DictReader(StringIO(content))
        raw_data = [row for row in reader]
    else:
        raw_data = [json.loads(line) for line in content.strip().split("\n") if line.strip()]

    cleaner = EnterpriseDataCleaner(raw_data)
    cleaned_result = cleaner.process()
    
    return cleaner.export_api_payload(cleaned_result)
