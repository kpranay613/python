from flask import Flask, request
import os
import re
import multiprocessing

app = Flask(__name__)

# Define mapper function
def mapper(data_chunk):
    word_counts = {}
    # Split the input data chunk into words using regular expressions
    words = re.findall(r'\w+', data_chunk.lower())
    # Count the number of occurrences of each word in the data chunk
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

# Define reducer function
def reducer(results):
    word_count = {}
    # Merge the word counts from each data chunk
    for result in results:
        for word, count in result.items():
            if word in word_count:
                word_count[word] += count
            else:
                word_count[word] = count
    return word_count

@app.route('/', methods=['GET', 'POST'])
def index():
    html = '''
    <!doctype html>
    <html>
        <body>
            <h1>Upload a Text File to process on Map Reduce Flow</h1>
            <form method="post" enctype="multipart/form-data" action="/upload">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    '''
    return html

@app.route('/upload', methods=['POST'])
def upload_file():
    # Save uploaded file to local disk
    f = request.files['file']
    filename = f.filename
    f.save(filename)

    # Read data from file and split into chunks for mapping
    with open(filename, 'r') as f:
        data = f.read()
    data_chunks = [chunk for chunk in data.split(os.linesep) if chunk]

    # Create a pool of workers for mapping
    pool = multiprocessing.Pool()

    # Map data chunks to workers
    results = pool.map(mapper, data_chunks)

    # Reduce results
    word_count = reducer(results)

    # Sort word counts by frequency in descending order
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

    # Generate HTML table to display results
    table = '<table border="1" style="font-size: 16px"><tr><th>Word</th><th>Count</th></tr>'
    for word, count in sorted_word_count:
        table += f'<tr><td>{word}</td><td>{count}</td></tr>'
    table += '</table>'

    # Generate HTML for results page
    html = f'''
    <!doctype html>
    <html>
        <body>
            <h1>Results afer Map Reduce </h1>
            {table}
        </body>
    </html>
    '''

    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
