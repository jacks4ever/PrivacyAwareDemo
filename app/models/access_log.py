from datetime import datetime
from app import db

class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    endpoint = db.Column(db.String(256))
    method = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))
    accessed_data = db.Column(db.Text)
    is_privacy_leak = db.Column(db.Boolean, default=False)
    leak_type = db.Column(db.String(50), nullable=True)
    
    def __init__(self, endpoint, method, ip_address, user_agent, accessed_data, 
                 user_id=None, is_privacy_leak=False, leak_type=None):
        self.endpoint = endpoint
        self.method = method
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.accessed_data = accessed_data
        self.is_privacy_leak = is_privacy_leak
        self.leak_type = leak_type
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'endpoint': self.endpoint,
            'method': self.method,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'accessed_data': self.accessed_data,
            'is_privacy_leak': self.is_privacy_leak,
            'leak_type': self.leak_type
        }