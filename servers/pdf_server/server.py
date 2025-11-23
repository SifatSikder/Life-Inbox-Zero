import sys
import json
import fitz  # PyMuPDF
import base64
import io

def process_request(request):
    try:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "extract_pdf_text":
            pdf_data = params.get("pdf_data")
            if not pdf_data:
                return {"error": "Missing pdf_data"}
            
            try:
                pdf_bytes = base64.b64decode(pdf_data)
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                return {"result": {"text": text}}
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": "Method not found"}
    except Exception as e:
        return {"error": str(e)}

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line)
            response = process_request(request)
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception:
            break

if __name__ == "__main__":
    main()
