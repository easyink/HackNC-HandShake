from server.config import db

connections = db.Table(
    'connections',
    db.Column('user_id', db.String, db.ForeignKey('users.id'), primary_key=True),
    db.Column('connection_id', db.String, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.String(500))
    interests = db.Column(db.JSON)
    songs = db.Column(db.JSON)

    outgoing_connections = db.relationship(
        'User',
        secondary=connections,
        primaryjoin=(id == connections.c.user_id),
        secondaryjoin=(id == connections.c.connection_id),
        backref=db.backref('incoming_connections', lazy='dynamic'),
        lazy='dynamic'
    )
    
    # handshake_card as JSON
    handshake_card = db.Column(db.JSON, nullable=False, default={
        "design": 0, "color": "#FFFFFF"
    })
    
    instagram = db.Column(db.String(120), unique=True)
    snapchat = db.Column(db.String(120), unique=True)
    other = db.Column(db.String(120))

    def __init__(self, name, phone_number, id=None, bio=None, interests=None, songs=None, 
                 handshake_card=None, instagram=None, snapchat=None, other=None):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.bio = bio
        self.interests = interests if interests else []
        self.songs = songs if songs else []
        self.handshake_card = handshake_card if handshake_card else {"design": 0, "color": "#FFFFFF"}
        self.instagram = instagram
        self.snapchat = snapchat
        self.other = other
