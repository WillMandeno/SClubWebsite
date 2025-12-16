import os
from dotenv import load_dotenv
# package-relative imports so this script can be run as a module: python -m backend.scripts.create_admin
from ..database import SessionLocal, engine, Base
from ..models import User
from passlib.context import CryptContext

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    Base.metadata.create_all(bind=engine)
    
    admin_email = "willmandeno@gmail.com"
    admin_display_name = "Will Mandeno"
    admin_password = os.getenv("ADMIN_PASSWORD", "password")
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.display_name == admin_display_name).first()
        if existing:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email=admin_email,
            display_name=admin_display_name,
            hashed_password=hash_password(admin_password),
            is_admin=True
        )
        
        db.add(admin)
        db.commit()
        
        print("✓ Admin user created successfully!")
        print(f"  Email: {admin_email}")
        print(f"  Display name: {admin_display_name}")
        print(f"  Password: {admin_password}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()