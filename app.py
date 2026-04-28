import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from database import Database
from config import DEBUG, PORT
from ui.routes import APIRoutes, VectorRoutes

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'ui', 'static')
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')
CORS(app)

# Initialize database on startup
with app.app_context():
    Database.init_database()

# ============== HOME ENDPOINT ==============
app.route('/', methods=['GET'])(APIRoutes.home)

# ============== GET ENDPOINTS ==============
app.route('/api/cameras', methods=['GET'])(APIRoutes.get_cameras)
app.route('/api/cameras/<int:camera_id>', methods=['GET'])(APIRoutes.get_camera)
app.route('/api/cameras/search/<term>', methods=['GET'])(APIRoutes.search_cameras)
app.route('/api/cameras/status/<status>', methods=['GET'])(APIRoutes.get_cameras_by_room)
app.route('/api/stats', methods=['GET'])(APIRoutes.get_stats)

# ============== POST ENDPOINTS ==============
app.route('/api/cameras', methods=['POST'])(APIRoutes.create_camera)

# ============== PUT ENDPOINTS ==============
app.route('/api/cameras/<int:camera_id>', methods=['PUT'])(APIRoutes.update_camera)

# ============== DELETE ENDPOINTS ==============
app.route('/api/cameras/<int:camera_id>', methods=['DELETE'])(APIRoutes.delete_camera)

# ============== VECTOR SEARCH ENDPOINTS ==============
app.route('/api/vector/status',           methods=['GET'])(VectorRoutes.status)
app.route('/api/vector/search/text',      methods=['POST'])(VectorRoutes.search_text)
app.route('/api/vector/search/image',     methods=['POST'])(VectorRoutes.search_image)
app.route('/api/vector/search/hybrid',    methods=['POST'])(VectorRoutes.search_hybrid)
app.route('/api/vector/index/all',        methods=['POST'])(VectorRoutes.index_all)

# ============== ERROR HANDLERS ==============
app.errorhandler(404)(APIRoutes.not_found)
app.errorhandler(500)(APIRoutes.internal_error)

if __name__ == '__main__':
    print(f"Starting Cameras API on http://localhost:{PORT}")
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
