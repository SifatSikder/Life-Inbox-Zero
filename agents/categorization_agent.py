import google.generativeai as genai
import json

class CategorizationAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        self.schema = {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["event", "task", "bill", "document", "link", "reminder"]},
                "title": {"type": "string"},
                "confidence": {"type": "number"},
                "metadata": {"type": "object"}
            }
        }

    def classify_item(self, text):
        prompt = f"""
        Classify the following content into one of: Event, Task, Bill, Document, Link, Reminder.
        Extract relevant fields (date, amount, etc.) into metadata.
        
        Content:
        {text}
        
        Return JSON.
        """
        
        # In a real scenario, we would enforce JSON schema output if supported, 
        # or parse the text response.
        response = self.model.generate_content(prompt)
        try:
            # Simple cleanup to extract JSON if wrapped in markdown
            content = response.text.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            return json.loads(content)
        except:
            return {"category": "unknown", "raw_response": response.text}

    def run(self, extracted_items):
        categorized_items = []
        for item in extracted_items:
            classification = self.classify_item(item['text'])
            categorized_items.append({
                "file": item['file'],
                "classification": classification
            })
        return categorized_items

if __name__ == "__main__":
    pass
