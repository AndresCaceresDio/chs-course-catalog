from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image, ImageFile
import numpy as np
import webcolors
from collections import defaultdict
import itertools
from sklearn.cluster import KMeans
from multiprocessing import Pool, cpu_count
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def closest_color_name(requested_color):
    min_distance = float('inf')
    closest_name = None
    for hex_value, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        distance = (r_c - requested_color[0]) ** 2 + (g_c - requested_color[1]) ** 2 + (b_c - requested_color[2]) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

def categorize_color(color, centroids):
    r, g, b, a = color
    if a == 0:
        return None
    closest_centroid = min(centroids, key=lambda centroid: np.linalg.norm(centroid - np.array([r, g, b])))
    closest_name = closest_color_name(closest_centroid)
    return closest_name, rgb_to_hex(r, g, b)

def categorize_colors(image_path, n_clusters=10):
    try:
        image = Image.open(image_path).convert("RGBA")
    except (OSError, IOError) as e:
        print(f"Error opening image: {e}")
        return {}
    
    pixels = np.array(image)
    unique_colors = np.unique(pixels.reshape(-1, pixels.shape[2]), axis=0)
    non_transparent_colors = np.array([color[:3] for color in unique_colors if color[3] != 0])
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(non_transparent_colors)
    centroids = kmeans.cluster_centers_
    with Pool(cpu_count()) as pool:
        color_categories = pool.starmap(categorize_color, zip(unique_colors, itertools.repeat(centroids)))
    color_dict = defaultdict(list)
    for category, hex_color in filter(lambda x: x[0] is not None, color_categories):
        color_dict[category].append(hex_color)
    return color_dict

def process_row(y, pixels, hex_colors_to_remove):
    row = pixels[y]
    for x in range(row.shape[0]):
        if rgb_to_hex(*row[x][:3]) in hex_colors_to_remove:
            row[x] = (0, 0, 0, 0)
    return row

def remove_color_categories(input_image_path, output_image_path, categories, color_dict):
    hex_colors_to_remove = set(itertools.chain.from_iterable(color_dict[category] for category in categories))
    try:
        image = Image.open(input_image_path).convert("RGBA")
    except (OSError, IOError) as e:
        print(f"Error opening image: {e}")
        return None
    
    pixels = np.array(image)
    with Pool(cpu_count()) as pool:
        processed_rows = pool.starmap(process_row, zip(range(pixels.shape[0]), itertools.repeat(pixels), itertools.repeat(hex_colors_to_remove)))
    new_image = Image.fromarray(np.array(processed_rows), "RGBA")
    new_image.save(output_image_path, "PNG")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        color_dict = categorize_colors(filepath, n_clusters=10)
        if not color_dict:
            return jsonify({'error': 'Failed to process the image. Please try with another image.'})
        return jsonify({'filename': filename, 'color_dict': color_dict})
    return jsonify({'error': 'Invalid file type'})

@app.route('/remove', methods=['POST'])
def remove():
    data = request.get_json()
    categories = data['categories']
    filename = data['filename']
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    output_filename = f"output_{filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    color_dict = categorize_colors(input_path, n_clusters=10)
    if not color_dict:
        return jsonify({'error': 'Failed to process the image for removal. Please try with another image.'})
    remove_color_categories(input_path, output_path, categories, color_dict)
    return jsonify({'output_filename': output_filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
