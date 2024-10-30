from flask import Flask, render_template, request, Response, send_from_directory
from detect_crack import detect_crack, detect_objects, gen_frames
from recommendation import get_recommendations
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        object_type = request.form.get('object_type')
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Detect cracks and objects
            crack_length, crack_image_path = detect_crack(filepath)
            detected_objects, detected_image_path = detect_objects(filepath)
            
            # Get recommendations based on the crack length and selected object type
            recommendations = get_recommendations(crack_length, object_type)
            
            return render_template('index.html', uploaded=True, crack_length=crack_length,
                                   crack_image_path=os.path.basename(crack_image_path),
                                   detected_image_path=os.path.basename(detected_image_path),
                                   recommendations=recommendations,
                                   detected_objects=detected_objects)
    return render_template('index.html', uploaded=False)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Route for webcam-based real-time crack detection
@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
