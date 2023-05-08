from io import BytesIO
from flask import Flask, render_template, request
from PIL import Image, ImageOps, ImageFilter

from base64 import b64encode

app = Flask(__name__)

index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Converter</title>
</head>
<body>
    <h1>Image Converter</h1>
    <form action="/convert" method="post" enctype="multipart/form-data">
        <label>Select an image to convert:</label>
        <input type="file" name="image">
        <br>
        <label>Choose a conversion type:</label>
        <select name="conversion">
            <option value="grayscale">Grayscale</option>
            <option value="negative">Negative</option>
            <option value="cartoon">Cartoon</option>
        </select>
        <br>
        <button type="submit">Convert Image</button>
    </form>
</body>
</html>
"""

result_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Result</title>
</head>
<body>
    <h1>Image Result</h1>
    <img src="data:image/png;base64,{{ image }}" alt="Converted Image">
</body>
</html>
"""

@app.route('/')
def index():
    return index_html

@app.route('/convert', methods=['POST'])
def convert():
    img = Image.open(request.files['image'])

    conversion = request.form.get('conversion')
    if conversion == 'grayscale':
        img = img.convert('L')
    elif conversion == 'negative':
        img = ImageOps.invert(img)
    elif conversion == 'cartoon':
        # Apply edge enhancement filter
        img = img.filter(ImageFilter.FIND_EDGES)
        # Apply median filter for smoothing
        img = img.filter(ImageFilter.MedianFilter())
        # Apply posterization filter for cartoon effect
        img = img.quantize(colors=8)

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_base64 = b64encode(img_bytes.getvalue()).decode('ascii')
    result = result_html.replace('{{ image }}', img_base64)
    return result

if __name__ == '__main__':
    app.run(host='10.5.0.5', port=80)

if __name__ == '__main__':
   app.run(debug=True)
