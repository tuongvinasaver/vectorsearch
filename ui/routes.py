"""
API Route Handlers
Maps all Flask routes to their controller logic.
"""

from flask import jsonify, request, send_from_directory
import os
import time
import numpy as np
from embeddings import EmbeddingEngine
from vector_store import VectorStore
from crud import CamerasCRUD

UPLOAD_FOLDER = os.path.join('ui', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_upload(file):
    if not file or file.filename == '': return ''
    filename = secure_filename(f"{int(time.time())}_{file.filename}")
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return f"/static/uploads/{filename}"

def _engine() -> EmbeddingEngine: return EmbeddingEngine()
def _store()  -> VectorStore:      return VectorStore()

def _index_camera(camera: dict):
    """Embed camera and upsert to vector store. Combines image and text if available."""
    if not camera: return
    _batch_index_cameras([camera])

def _batch_index_cameras(cameras: list):
    """Embed multiple cameras in batches and upsert to vector store. Efficiently handles large lists."""
    if not cameras: return 0
    
    try:
        engine = _engine()
        store = _store()
        
        # 1. Batch embed texts
        texts = [engine.camera_to_text(c) for c in cameras]
        text_embs = engine.embed_text_batch(texts)
        
        # 2. Collect and batch embed images
        img_indices = []
        img_inputs = []
        for i, cam in enumerate(cameras):
            img_path = cam.get('image')
            if img_path:
                # Remove leading slash and join with root (assuming 'ui' is the web root)
                rel_path = img_path.lstrip('/')
                full_path = os.path.join('ui', rel_path)
                if os.path.exists(full_path):
                    img_indices.append(i)
                    img_inputs.append(full_path)
        
        img_embs = engine.embed_image_batch(img_inputs)
        img_emb_map = {idx: emb for idx, emb in zip(img_indices, img_embs)}
        
        # 3. Combine and prepare for storage
        final_embs = []
        ids = []
        metas = []
        
        for i, cam in enumerate(cameras):
            t_emb = text_embs[i]
            
            if i in img_emb_map:
                i_emb = img_emb_map[i]
                # Combine image and text embeddings, prioritizing text (70% text, 30% image)
                t_norm = np.array(t_emb) / (np.linalg.norm(t_emb) + 1e-9)
                i_norm = np.array(i_emb) / (np.linalg.norm(i_emb) + 1e-9)
                combined = (t_norm * 0.7) + (i_norm * 0.3)
                final_embs.append(combined.tolist())
            else:
                final_embs.append(t_emb)
                
            ids.append(cam['id'])
            metas.append(cam)
        
        store.upsert_batch(ids, final_embs, metas)
        return len(ids)
    except Exception as exc:
        print(f"[routes] Batch index failed: {exc}")
        return 0


class APIRoutes:
    """All API route handler methods"""

    # ── HOME ──────────────────────────────────────────────────────────────────
    @staticmethod
    def home():
        """Serve the frontend HTML UI"""
        ui_dir = os.path.join(os.path.dirname(__file__), 'static')
        return send_from_directory(ui_dir, 'index.html')

    # ── GET ───────────────────────────────────────────────────────────────────
    @staticmethod
    def get_cameras():
        """GET /api/cameras — Return all cameras (supports ?limit= & ?offset=)"""
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)
        cameras = CamerasCRUD.read_all(limit=limit, offset=offset)
        return jsonify({'success': True, 'count': len(cameras), 'cameras': cameras})

    @staticmethod
    def get_camera(camera_id):
        """GET /api/cameras/<id> — Return a single camera"""
        camera = CamerasCRUD.read_by_id(camera_id)
        if not camera:
            return jsonify({'success': False, 'message': 'Camera not found'}), 404
        return jsonify({'success': True, 'camera': camera})

    @staticmethod
    def search_cameras(term):
        """GET /api/cameras/search/<term> — Keyword search by name or location"""
        cameras = CamerasCRUD.search(term)
        return jsonify({'success': True, 'count': len(cameras), 'cameras': cameras})

    @staticmethod
    def get_cameras_by_room(status):
        """GET /api/cameras/status/<status> — Filter cameras by status"""
        query_map = {
            'active':   "SELECT * FROM cameras WHERE status = 'active' ORDER BY created_at DESC",
            'inactive': "SELECT * FROM cameras WHERE status = 'inactive' ORDER BY created_at DESC",
        }
        from database import Database
        cameras = Database.fetch_all(
            query_map.get(status, "SELECT * FROM cameras ORDER BY created_at DESC")
        )
        return jsonify({'success': True, 'count': len(cameras), 'cameras': cameras})

    @staticmethod
    def get_stats():
        """GET /api/stats — Dashboard statistics"""
        from database import Database
        total = CamerasCRUD.count()
        active_res   = Database.fetch_one("SELECT COUNT(*) as count FROM cameras WHERE status = 'active'")
        inactive_res = Database.fetch_one("SELECT COUNT(*) as count FROM cameras WHERE status = 'inactive'")
        active   = active_res['count']   if active_res   else 0
        inactive = inactive_res['count'] if inactive_res else 0
        return jsonify({'success': True, 'stats': {'total': total, 'active': active, 'inactive': inactive}})

    # ── POST ──────────────────────────────────────────────────────────────────
    @staticmethod
    def create_camera():
        """POST /api/cameras — Create a new camera with optional image upload"""
        # Handle multipart/form-data
        name       = request.form.get('name')
        location   = request.form.get('location')
        ip_address = request.form.get('ip_address')
        
        if not all([name, location, ip_address]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400

        image_path = ''
        if 'image' in request.files:
            image_path = save_upload(request.files['image'])

        camera_id = CamerasCRUD.create(
            name=name,
            location=location,
            ip_address=ip_address,
            status=request.form.get('status', 'active'),
            resolution=request.form.get('resolution', ''),
            image=image_path
        )
        
        if camera_id is None:
            return jsonify({'success': False, 'message': 'Failed to create camera (IP may already exist)'}), 500

        camera = CamerasCRUD.read_by_id(camera_id)
        _index_camera(camera)   # ← auto-index (now uses image if uploaded!)
        return jsonify({'success': True, 'camera': camera}), 201

    # ── PUT ───────────────────────────────────────────────────────────────────
    @staticmethod
    def update_camera(camera_id):
        """PUT /api/cameras/<id> — Update camera with optional image upload"""
        existing = CamerasCRUD.read_by_id(camera_id)
        if not existing:
            return jsonify({'success': False, 'message': 'Camera not found'}), 404

        # Use request.form for multipart data
        allowed = ['name', 'location', 'ip_address', 'status', 'resolution']
        updates = {k: request.form.get(k) for k in allowed if k in request.form}
        
        if 'image' in request.files:
            updates['image'] = save_upload(request.files['image'])

        if not updates:
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400

        # Sync with DB
        camera = CamerasCRUD.update(camera_id, **updates)
        if not camera:
            return jsonify({'success': False, 'message': 'Failed to update database'}), 500

        _index_camera(camera)   # ← re-index (now uses new image if uploaded!)
        return jsonify({'success': True, 'camera': camera})

    # ── DELETE ────────────────────────────────────────────────────────────────
    @staticmethod
    def delete_camera(camera_id):
        """DELETE /api/cameras/<id> — Delete camera and remove from vector index"""
        existing = CamerasCRUD.read_by_id(camera_id)
        if not existing:
            return jsonify({'success': False, 'message': 'Camera not found'}), 404

        CamerasCRUD.delete(camera_id)
        _store().delete(camera_id)   # ← remove from index
        return jsonify({'success': True, 'message': f'Camera {camera_id} deleted successfully'})

    # ── ERROR HANDLERS ────────────────────────────────────────────────────────
    @staticmethod
    def not_found(e):
        return jsonify({'success': False, 'message': 'Endpoint not found', 'error': str(e)}), 404

    @staticmethod
    def internal_error(e):
        return jsonify({'success': False, 'message': 'Internal server error', 'error': str(e)}), 500


# ══════════════════════════════════════════════════════════════════════════════
# VECTOR SEARCH ROUTES
# ══════════════════════════════════════════════════════════════════════════════

class VectorRoutes:
    """Vector search endpoints"""

    @staticmethod
    def status():
        """GET /api/vector/status — Index info"""
        try:
            count = _store().count()
            return jsonify({'success': True, 'indexed': count, 'model': 'clip-ViT-B-32'})
        except Exception as exc:
            return jsonify({'success': False, 'message': str(exc)}), 500

    @staticmethod
    def search_text():
        data = request.get_json()
        if not data or not data.get('query'):
            return jsonify({'success': False, 'message': 'query field required'}), 400

        query = data['query'].strip()
        limit = int(data.get('limit', 10))
        status = data.get('status')
        threshold = float(data.get('threshold', 0.0))
        use_rerank = data.get('rerank', True)

        where = {"status": status} if status and status != 'all' else None

        try:
            #  1. Embed query
            vec = _engine().embed_text(query)

            #  2. ANN retrieval
            fetch_limit = max(50, limit * 3) if use_rerank else limit
            matches = _store().search(vec, n_results=fetch_limit, where=where)

            if not matches:
                return jsonify({'success': True, 'count': 0, 'cameras': []})

            #  Normalize ANN score (distance → similarity)
            for m in matches:
                if 'distance' in m:
                    m['vector_score'] = 1 - float(m['distance'])  # cosine distance → similarity
                else:
                    m['vector_score'] = m.get('score', 0.0)

            #  3. Re-ranking
            if use_rerank and len(matches) > 1:
                cameras_data = [CamerasCRUD.read_by_id(m['camera_id']) for m in matches]
                valid_pairs = [(m, c) for m, c in zip(matches, cameras_data) if c]

                if valid_pairs:
                    matches_v, cameras_v = zip(*valid_pairs)
                    docs = [_engine().camera_to_text(c) for c in cameras_v]

                    rerank_scores = _engine().rerank(query, docs)

                    #  Normalize rerank scores (min-max instead of sigmoid)
                    min_s = min(rerank_scores)
                    max_s = max(rerank_scores)
                    range_s = max_s - min_s if max_s != min_s else 1.0

                    for i, m in enumerate(matches_v):
                        rerank_score = (rerank_scores[i] - min_s) / range_s
                        m['rerank_score'] = float(rerank_score)

                        #  Combine vector + rerank (weighted)
                        m['score'] = 0.4 * m['vector_score'] + 0.6 * m['rerank_score']
                        m['is_reranked'] = True

                    matches = list(matches_v)

            else:
                # fallback nếu không rerank
                for m in matches:
                    m['score'] = m['vector_score']

            #  4. Sort final
            matches.sort(key=lambda x: x['score'], reverse=True)

            #  5. Apply threshold
            final = [m for m in matches if m['score'] >= threshold]

            return _enrich_results(final[:limit])

        except Exception as exc:
            return jsonify({'success': False, 'message': str(exc)}), 500

    @staticmethod
    def search_image():
        """POST /api/vector/search/image — Image similarity search"""
        limit     = 10
        status    = None
        threshold = 0.0
        
        try:
            if request.content_type and 'multipart' in request.content_type:
                if 'image' not in request.files:
                    return jsonify({'success': False, 'message': 'No image file provided'}), 400
                f         = request.files['image']
                limit     = int(request.form.get('limit', 10))
                status    = request.form.get('status')
                threshold = float(request.form.get('threshold', 0.0))
                vec       = _engine().embed_image_bytes(f.read())
            else:
                data      = request.get_json() or {}
                limit     = int(data.get('limit', 10))
                status    = data.get('status')
                threshold = float(data.get('threshold', 0.0))
                if data.get('url'):
                    vec = _engine().embed_image_url(data['url'])
                elif data.get('b64'):
                    vec = _engine().embed_image_b64(data['b64'])
                else:
                    return jsonify({'success': False, 'message': 'Provide image file, url, or b64'}), 400

            where = {"status": status} if status and status != 'all' else None
            matches = _store().search(vec, n_results=limit, where=where)
            return _enrich_results(matches, min_score=threshold)
        except Exception as exc:
            return jsonify({'success': False, 'message': str(exc)}), 500

    @staticmethod
    def search_hybrid():
        """POST /api/vector/search/hybrid — Combines Keyword + Semantic search
        Body: { "query": "...", "limit": 10, "status": "...", "threshold": 0.0 }
        """
        data = request.get_json()
        if not data or not data.get('query'):
            return jsonify({'success': False, 'message': 'query field required'}), 400

        query     = data['query'].strip()
        limit     = int(data.get('limit', 10))
        status    = data.get('status')
        threshold = float(data.get('threshold', 0.0))

        where = {"status": status} if status and status != 'all' else None

        try:
            # 1. Semantic Retrieval
            vec       = _engine().embed_text(query)
            v_matches = _store().search(vec, n_results=limit * 4, where=where) 
            
            # 2. Keyword Retrieval
            k_cameras = CamerasCRUD.search(query)
            k_ids     = {c['id'] for c in k_cameras}

            # 3. Hybrid Merging
            merged_ids = set()
            candidates = []

            for m in v_matches:
                cam_id = m['camera_id']
                if cam_id in k_ids:
                    m['hybrid_boost'] = 0.2
                else:
                    m['hybrid_boost'] = 0.0
                candidates.append(m)
                merged_ids.add(cam_id)

            for k_cam in k_cameras:
                if k_cam['id'] not in merged_ids:
                    if status and status != 'all' and k_cam['status'] != status:
                        continue
                    candidates.append({
                        'camera_id': k_cam['id'],
                        'score': 0.4, # Base score for keyword matches
                        'hybrid_boost': 0.1,
                        'metadata': {},
                        'distance': 1.0
                    })

            if not candidates:
                return jsonify({'success': True, 'count': 0, 'cameras': []})

            # 4. Re-ranking the hybrid candidates
            cameras_data = [CamerasCRUD.read_by_id(c['camera_id']) for c in candidates]
            valid_pairs = [(m, c) for m, c in zip(candidates, cameras_data) if c]
            
            if valid_pairs:
                candidates_v, cameras_v = zip(*valid_pairs)
                docs = [_engine().camera_to_text(c) for c in cameras_v]
                rerank_scores = _engine().rerank(query, docs)
                
                for i, m in enumerate(candidates_v):
                    base_score = 1 / (1 + np.exp(-rerank_scores[i]))
                    m['score'] = min(1.0, base_score + m.get('hybrid_boost', 0.0))
                    m['is_reranked'] = True
                
                final_matches = list(candidates_v)
                final_matches.sort(key=lambda x: x['score'], reverse=True)
            else:
                final_matches = candidates

            return _enrich_results(final_matches[:limit], min_score=threshold)
        except Exception as exc:
            return jsonify({'success': False, 'message': str(exc)}), 500

    @staticmethod
    def index_all():
        """POST /api/vector/index/all — Re-index every camera (uses images if available)"""
        try:
            cameras = CamerasCRUD.read_all()
            indexed_count = _batch_index_cameras(cameras)
            
            return jsonify({
                'success': True, 
                'indexed': indexed_count, 
                'total': len(cameras),
                'message': f'Successfully re-indexed {indexed_count} cameras using batch optimization.'
            })
        except Exception as exc:
            return jsonify({'success': False, 'message': str(exc)}), 500


def _enrich_results(matches: list, min_score: float = 0.0):
    """Fetch full camera rows from MySQL and merge similarity scores."""
    enriched = []
    for m in matches:
        if m['score'] < min_score:
            continue
        cam = CamerasCRUD.read_by_id(m['camera_id'])
        if cam:
            cam['score']    = m['score']
            cam['distance'] = m.get('distance', 0.0)
            cam['metadata'] = m.get('metadata', {})
            cam['embedding'] = m.get('embedding', []) # Add embedding for inspection
            enriched.append(cam)
    return jsonify({'success': True, 'count': len(enriched), 'cameras': enriched})
