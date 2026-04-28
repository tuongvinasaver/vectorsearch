"""CRUD operations for database tables"""
from database import Database


class CamerasCRUD:
    """CRUD operations for cameras table"""
    
    @staticmethod
    def create(name, rtsp_url, room_id=None, room_name=None, image=None):
        """Create a new camera record"""
        query = """
        INSERT INTO cameras (name, rtsp_url, room_id, room_name, image)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (name, rtsp_url, room_id, room_name, image if image else '')
        result = Database.execute_query(query, params)
        
        if result:
            return {
                'id': result,
                'name': name,
                'rtsp_url': rtsp_url,
                'room_id': room_id,
                'room_name': room_name,
                'image': image
            }
        return None
    
    @staticmethod
    def read_all(limit=None, offset=0):
        """Read all camera records"""
        if limit:
            query = f"SELECT * FROM cameras ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
        else:
            query = "SELECT * FROM cameras ORDER BY created_at DESC"
        
        return Database.fetch_all(query)
    
    @staticmethod
    def read_by_id(camera_id):
        """Read a camera record by ID"""
        query = "SELECT * FROM cameras WHERE id = %s"
        return Database.fetch_one(query, (camera_id,))
    
    @staticmethod
    def read_by_rtsp(rtsp_url):
        """Read a camera record by RTSP URL"""
        query = "SELECT * FROM cameras WHERE rtsp_url = %s"
        return Database.fetch_one(query, (rtsp_url,))
    
    @staticmethod
    def search(search_term):
        """Search cameras by name or location"""
        query = """
        SELECT * FROM cameras 
        WHERE name LIKE %s OR location LIKE %s
        ORDER BY created_at DESC
        """
        params = (f"%{search_term}%", f"%{search_term}%")
        return Database.fetch_all(query, params)
    
    @staticmethod
    def update(camera_id, **kwargs):
        """Update a camera record"""
        allowed_fields = ['name', 'rtsp_url', 'room_id', 'room_name', 'image']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return None
        
        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        query = f"UPDATE cameras SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        params = tuple(list(updates.values()) + [camera_id])
        
        Database.execute_query(query, params)
        return CamerasCRUD.read_by_id(camera_id)
    
    @staticmethod
    def delete(camera_id):
        """Delete a camera record"""
        query = "DELETE FROM cameras WHERE id = %s"
        result = Database.execute_query(query, (camera_id,))
        return result is not None
    
    @staticmethod
    def get_by_room(room_id):
        """Get cameras by room"""
        query = "SELECT * FROM cameras WHERE room_id = %s ORDER BY created_at DESC"
        return Database.fetch_all(query, (room_id,))
    
    @staticmethod
    def count():
        """Get total number of cameras"""
        query = "SELECT COUNT(*) as count FROM cameras"
        result = Database.fetch_one(query)
        return result['count'] if result else 0
