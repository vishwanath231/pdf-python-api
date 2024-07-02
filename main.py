from flask import Flask, request, jsonify
import tabula
import pandas as pd
import os
import io

app = Flask(__name__)

@app.route('/extract-tables', methods=['POST'])
def extract_tables():
    # Check if a file is provided
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']

    # Save the file locally
    file_path = "temp.pdf"
    file.save(file_path)

    # Extract tables from PDF
    df_list = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

    # Combine all tables into a single DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)

    # Convert the DataFrame to JSON
    json_data = combined_df.to_dict(orient="records")

    # Remove the PDF file
    os.remove(file_path)

    # Return the JSON data as response
    return jsonify(json_data)

if __name__ == '__main__':
    app.run(debug=True)
