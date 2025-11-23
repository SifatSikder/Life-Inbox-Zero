import sys
import json
import pytesseract
from PIL import Image
import io
import base64

def process_request(request):
    try:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "ocr_image":
            image_data = params.get("image_data")
            if not image_data:
                return {"error": "Missing image_data"}
            
            try:
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                text = pytesseract.image_to_string(image)
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
