import streamlit as st
import json
import csv
from io import StringIO
from cleaner import EnterpriseDataCleaner 

st.set_page_config(page_title="AI Data Cleaner SaaS", page_icon="🧹", layout="wide")

st.title("🧹 منظف بيانات الذكاء الاصطناعي (Micro-SaaS)")
st.write("ارفع ملف البيانات لمعالجته، إزالة الضوضاء، واستخراج ملف JSONL جاهز للتدريب.")

uploaded_file = st.file_uploader("اختر ملف البيانات (CSV / JSONL)", type=["csv", "jsonl"])

if uploaded_file is not None:
    content = uploaded_file.getvalue().decode("utf-8")
    raw_data = []

    if uploaded_file.name.endswith(".csv"):
        reader = csv.DictReader(StringIO(content))
        raw_data = [row for row in reader]
    else:
        raw_data = [json.loads(line) for line in content.strip().split("\n") if line.strip()]

    if st.button("بدء التنظيف والمعالجة 🚀"):
        cleaner = EnterpriseDataCleaner(raw_data)
        cleaned_data = cleaner.process()
        payload = cleaner.export_api_payload(cleaned_data)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي المدخلات", payload["metrics"]["total_input"])
        col2.metric("البيانات المقبولة", payload["metrics"]["cleaned_output"])
        col3.metric("مؤشر الجودة", f"{payload['metrics']['health_score']}%")

        st.success("تمت المعالجة بنجاح!")
        
        st.download_button(
            label="📥 تحميل ملف JSONL المنظف",
            data=payload["jsonl_data"],
            file_name="cleaned_dataset.jsonl",
            mime="application/jsonlines"
        )
