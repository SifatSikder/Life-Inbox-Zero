import json
import subprocess
import base64
import os

class ExtractionAgent:
    def __init__(self):
        self.ocr_server_cmd = ["python", "servers/ocr_server/server.py"]
        self.pdf_server_cmd = ["python", "servers/pdf_server/server.py"]

    def call_mcp_server(self, cmd, method, params):
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        request = {"method": method, "params": params}
        stdout, stderr = process.communicate(input=json.dumps(request) + "\n")
        
        if stderr:
            print(f"Error calling MCP server: {stderr}")
            return None
            
        try:
            response = json.loads(stdout)
            return response.get("result")
        except json.JSONDecodeError:
            return None

    def extract_from_image(self, image_path):
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        result = self.call_mcp_server(
            self.ocr_server_cmd,
            "ocr_image",
            {"image_data": image_data}
        )
        return result.get("text") if result else ""

    def extract_from_pdf(self, pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = base64.b64encode(f.read()).decode("utf-8")
        
        result = self.call_mcp_server(
            self.pdf_server_cmd,
            "extract_pdf_text",
            {"pdf_data": pdf_data}
        )
        return result.get("text") if result else ""

    def run(self, files):
        results = []
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            text = ""
            if ext in ['.png', '.jpg', '.jpeg']:
                text = self.extract_from_image(file_path)
            elif ext == '.pdf':
                text = self.extract_from_pdf(file_path)
            
            results.append({
                "file": file_path,
                "text": text
            })
        return results

if __name__ == "__main__":
    # Test
    pass
