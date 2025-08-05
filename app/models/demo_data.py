from app import db
from app.models.user import User
from app.models.post import Post

def initialize_demo_data():
    """Initialize demo data if the database is empty"""
    # Check if we already have users
    if User.query.count() > 0:
        return
        
    print("Initializing demo data...")
    
    # Create admin user
    admin = User(
        username="admin",
        email="admin@example.com",
        password="adminpass",
        bio="System administrator",
        is_admin=True
    )
    admin.email_public = False
    admin.bio_public = True
    db.session.add(admin)
    
    # Create regular users with different privacy settings
    alice = User(
        username="alice",
        email="alice@example.com",
        password="alicepass",
        bio="Hi, I'm Alice! I love sharing my thoughts and ideas."
    )
    alice.email_public = True  # Alice makes her email public
    alice.bio_public = True
    db.session.add(alice)
    
    bob = User(
        username="bob",
        email="bob@example.com",
        password="bobpass",
        bio="Privacy advocate. I keep my information private."
    )
    bob.email_public = False  # Bob keeps his email private
    bob.bio_public = True
    db.session.add(bob)
    
    charlie = User(
        username="charlie",
        email="charlie@example.com",
        password="charliepass",
        bio="Very private person. Please respect my privacy."
    )
    charlie.email_public = False  # Charlie keeps everything private
    charlie.bio_public = False
    db.session.add(charlie)
    
    # Create some posts for each user
    # Alice's posts
    db.session.add(Post(
        title="Hello World!",
        content="This is my first public post on this platform!",
        user_id=2,  # Alice's ID
        is_public=True
    ))
    
    db.session.add(Post(
        title="My Private Thoughts",
        content="This is a private post that only I should be able to see.",
        user_id=2,  # Alice's ID
        is_public=False
    ))
    
    # Bob's posts
    db.session.add(Post(
        title="Privacy Matters",
        content="Here's why privacy is important in the digital age...",
        user_id=3,  # Bob's ID
        is_public=True
    ))
    
    db.session.add(Post(
        title="My Secret Project",
        content="I'm working on something exciting but want to keep it private for now.",
        user_id=3,  # Bob's ID
        is_public=False
    ))
    
    # Charlie's posts
    db.session.add(Post(
        title="Limited Sharing",
        content="I'm only sharing this with trusted friends.",
        user_id=4,  # Charlie's ID
        is_public=True
    ))
    
    db.session.add(Post(
        title="Personal Notes",
        content="These are my personal notes that should remain private.",
        user_id=4,  # Charlie's ID
        is_public=False
    ))
    
    # Create a "deleted" post that still exists in the database
    deleted_post = Post(
        title="Post Marked as Deleted",
        content="This post was 'deleted' but still exists in the database.",
        user_id=2,  # Alice's ID
        is_public=True
    )
    deleted_post.is_deleted = True
    db.session.add(deleted_post)
    
    # Commit all changes
    db.session.commit()
    print("Demo data initialized successfully!")