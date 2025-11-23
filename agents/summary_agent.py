from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class SummaryAgent:
    def __init__(self):
        self.output_dir = "summaries"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_digest(self, summary_data):
        filename = f"{self.output_dir}/weekly_digest.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        c.drawString(100, height - 50, "Life Inbox Zero - Weekly Digest")
        
        y = height - 100
        for key, value in summary_data.items():
            c.drawString(100, y, f"{key}: {value}")
            y -= 20
            
        c.save()
        return filename

    def run(self, processed_data):
        # Aggregate data
        summary = {
            "Total Items": len(processed_data),
            "Events Created": sum(1 for x in processed_data if x.get('category') == 'event'),
            "Bills Processed": sum(1 for x in processed_data if x.get('category') == 'bill'),
        }
        
        pdf_path = self.generate_digest(summary)
        return f"Digest generated at {pdf_path}"

if __name__ == "__main__":
    pass
