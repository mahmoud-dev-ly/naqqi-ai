import re
import json

class EnterpriseDataCleaner:
    def __init__(self, data):
        self.raw_data = data
        self.bad_words = ["سبام", "اعلان", "تواصل معنا", "إعلان", "حظر"]

    def remove_diacritics(self, text):
        arabic_diacritics = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
        return re.sub(arabic_diacritics, '', text)

    def clean_text(self, text):
        if not isinstance(text, str):
            return text
        
        text = self.remove_diacritics(text)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^\w\s\u0600-\u06FF]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def is_bad_content(self, text):
        if not text or len(text) < 3:
            return True
        for word in self.bad_words:
            if word in text:
                return True
        return False

    def process(self):
        cleaned_list = []
        seen_texts = set()

        for item in self.raw_data:
            text_content = item.get("text", "") if isinstance(item, dict) else str(item)
            cleaned = self.clean_text(text_content)

            if cleaned and not self.is_bad_content(cleaned):
                if cleaned not in seen_texts:
                    seen_texts.add(cleaned)
                    cleaned_list.append({"text": cleaned})

        return cleaned_list

    def export_api_payload(self, cleaned_result):
        total_input = len(self.raw_data)
        cleaned_output = len(cleaned_result)
        health_score = round((cleaned_output / total_input * 100), 2) if total_input > 0 else 0

        jsonl_lines = [json.dumps(row, ensure_ascii=False) for row in cleaned_result]
        jsonl_data = "\n".join(jsonl_lines)

        return {
            "status": "success",
            "metrics": {
                "total_input": total_input,
                "cleaned_output": cleaned_output,
                "health_score": health_score
            },
            "data": cleaned_result,
            "jsonl_data": jsonl_data
        }

if __name__ == "__main__":
    sample_data = [
        {"text": "مَرحباً بكَ في شَرِكتِنا! 🚀 https://example.com"},
        {"text": "هذا إعلان للبيع تواصل معنا"},
        {"text": "مَرحباً بكَ في شَرِكتِنا!"}
    ]
    cleaner = EnterpriseDataCleaner(sample_data)
    result = cleaner.process()
    print(cleaner.export_api_payload(result))
