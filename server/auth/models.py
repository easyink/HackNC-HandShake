from server.config import db

# Association table for the many-to-many relationship
connections = db.Table(
    'connections',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('connection_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=False, unique=True)
    bio = db.Column(db.String(500))
    interests = db.Column(db.JSON)
    songs = db.Column(db.JSON)
    
    # handshake_card as JSON
    handshake_card = db.Column(db.JSON, nullable=False, default={
        "design": 0, "color": "#FFFFFF"
    })
    
    instagram = db.Column(db.String(120), unique=True)
    snapchat = db.Column(db.String(120), unique=True)
    other = db.Column(db.String(120))
    
    # Many-to-many relationship with itself for connections
    connections = db.relationship(
        'User', secondary=connections,
        primaryjoin=(connections.c.user_id == id),
        secondaryjoin=(connections.c.connection_id == id),
        backref=db.backref('connected_to', lazy='dynamic'), lazy='dynamic'
    )

    def __init__(self, name, phone_number, bio=None, interests=None, songs=None, 
                 handshake_card=None, instagram=None, snapchat=None, other=None):
        self.name = name
        self.phone_number = phone_number
        self.bio = bio
        self.interests = interests if interests else []
        self.songs = songs if songs else []
        self.handshake_card = handshake_card if handshake_card else {"design": 0, "color": "#FFFFFF"}
        self.instagram = instagram
        self.snapchat = snapchat
        self.other = other

    def add_connection(self, user):
        """Add a connection if it doesn't already exist."""
        if not self.is_connected(user):
            self.connections.append(user)
            db.session.commit()

    def remove_connection(self, user):
        """Remove a connection if it exists."""
        if self.is_connected(user):
            self.connections.remove(user)
            db.session.commit()

    def is_connected(self, user):
        """Check if a connection exists."""
        return self.connections.filter(connections.c.connection_id == user.id).count() > 0
