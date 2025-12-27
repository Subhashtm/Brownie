from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uuid
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional, List
import json
from PIL import Image
import bcrypt

# Load environment variables
load_dotenv()

app = FastAPI(title="AniAthu's brownies API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Static file serving for Vercel
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    """Serve static files from frontend directory"""
    static_file_path = Path("frontend") / file_path
    
    if not static_file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine content type
    content_type = "text/plain"
    if file_path.endswith('.css'):
        content_type = "text/css"
    elif file_path.endswith('.js'):
        content_type = "application/javascript"
    elif file_path.endswith('.html'):
        content_type = "text/html"
    elif file_path.endswith('.png'):
        content_type = "image/png"
    elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        content_type = "image/jpeg"
    elif file_path.endswith('.gif'):
        content_type = "image/gif"
    elif file_path.endswith('.svg'):
        content_type = "image/svg+xml"
    
    return FileResponse(
        static_file_path,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=3600"}
    )

# Upload file serving for Vercel
@app.get("/uploads/{file_path:path}")
async def serve_uploads(file_path: str):
    """Serve uploaded files"""
    upload_file_path = Path("uploads") / file_path
    
    if not upload_file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine content type for images
    content_type = "application/octet-stream"
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        if file_path.lower().endswith('.png'):
            content_type = "image/png"
        elif file_path.lower().endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif file_path.lower().endswith('.gif'):
            content_type = "image/gif"
        elif file_path.lower().endswith('.webp'):
            content_type = "image/webp"
    
    return FileResponse(
        upload_file_path,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"}
    )

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    name: str
    description: str
    price: float
    image_url: Optional[str] = None
    category: str = "brownie"
    available: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None

class CartItem(BaseModel):
    product_id: int
    quantity: int

class ContactInfo(BaseModel):
    email: str
    phone: str
    address: str

class PaymentInfo(BaseModel):
    qr_code_url: str
    payment_email: str

# Helper functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_admin(email: str = Depends(verify_token)):
    if email != os.getenv("ADMIN_EMAIL"):
        raise HTTPException(status_code=403, detail="Admin access required")
    return email

def hash_password(password: str):
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = password.encode('utf-8')[:72]
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    # Truncate password to 72 bytes for bcrypt compatibility
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("frontend/index.html")

@app.post("/api/register")
async def register(user: UserCreate):
    try:
        # Check if user exists
        existing_user = supabase.table("users").select("*").eq("email", user.email).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        hashed_password = hash_password(user.password)
        result = supabase.table("users").insert({
            "email": user.email,
            "password": hashed_password,
            "name": user.name,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
async def login(user: UserLogin):
    try:
        # Check admin login
        if user.email == os.getenv("ADMIN_EMAIL") and user.password == os.getenv("ADMIN_PASSWORD"):
            access_token = create_access_token(data={"sub": user.email, "role": "admin"})
            return {"access_token": access_token, "token_type": "bearer", "role": "admin"}
        
        # Check regular user
        db_user = supabase.table("users").select("*").eq("email", user.email).execute()
        if not db_user.data or not verify_password(user.password, db_user.data[0]["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email, "role": "user"})
        return {"access_token": access_token, "token_type": "bearer", "role": "user"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/products")
async def get_products():
    try:
        result = supabase.table("products").select("*").eq("available", True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    try:
        result = supabase.table("products").select("*").eq("id", product_id).execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Product not found")
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/products")
async def create_product(product: Product, admin_email: str = Depends(verify_admin)):
    try:
        result = supabase.table("products").insert(product.dict()).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, admin_email: str = Depends(verify_admin)):
    try:
        update_data = {k: v for k, v in product.dict().items() if v is not None}
        result = supabase.table("products").update(update_data).eq("id", product_id).execute()
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/admin/products/{product_id}")
async def delete_product(product_id: int, admin_email: str = Depends(verify_admin)):
    try:
        supabase.table("products").delete().eq("id", product_id).execute()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/upload-image")
async def upload_image(file: UploadFile = File(...), admin_email: str = Depends(verify_admin)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            raise HTTPException(status_code=400, detail="Unsupported image format")
        
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Optimize image (resize if too large)
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = convert('RGB')
                
                # Resize if image is too large
                max_size = (800, 600)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(file_path, optimize=True, quality=85)
        except Exception as e:
            print(f"Image optimization failed: {e}")
        
        # Return the URL path
        image_url = f"/uploads/{unique_filename}"
        return {"image_url": image_url}
        
    except Exception as e:
        # Clean up file if it was created
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/cart/add")
async def add_to_cart(item: CartItem, email: str = Depends(verify_token)):
    try:
        # Check if item already in cart
        existing = supabase.table("cart").select("*").eq("user_email", email).eq("product_id", item.product_id).execute()
        
        if existing.data:
            # Update quantity
            new_quantity = existing.data[0]["quantity"] + item.quantity
            result = supabase.table("cart").update({"quantity": new_quantity}).eq("id", existing.data[0]["id"]).execute()
        else:
            # Add new item
            result = supabase.table("cart").insert({
                "user_email": email,
                "product_id": item.product_id,
                "quantity": item.quantity
            }).execute()
        
        return {"message": "Item added to cart"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/cart")
async def get_cart(email: str = Depends(verify_token)):
    try:
        result = supabase.table("cart").select("*, products(*)").eq("user_email", email).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/cart/{item_id}")
async def remove_from_cart(item_id: int, email: str = Depends(verify_token)):
    try:
        supabase.table("cart").delete().eq("id", item_id).eq("user_email", email).execute()
        return {"message": "Item removed from cart"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/contact")
async def get_contact_info():
    try:
        result = supabase.table("settings").select("*").eq("key", "contact_info").execute()
        if result.data:
            return json.loads(result.data[0]["value"])
        return {"email": "contact@brownieshop.com", "phone": "+91-9876543210", "address": "123 Brownie St"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/contact")
async def update_contact_info(contact: ContactInfo, admin_email: str = Depends(verify_admin)):
    try:
        # Upsert contact info
        result = supabase.table("settings").upsert({
            "key": "contact_info",
            "value": json.dumps(contact.dict())
        }).execute()
        return {"message": "Contact info updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/payment-info")
async def get_payment_info():
    try:
        result = supabase.table("settings").select("*").eq("key", "payment_info").execute()
        if result.data:
            return json.loads(result.data[0]["value"])
        return {"qr_code_url": "", "payment_email": "payments@brownieshop.com"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/admin/payment-info")
async def update_payment_info(payment: PaymentInfo, admin_email: str = Depends(verify_admin)):
    try:
        result = supabase.table("settings").upsert({
            "key": "payment_info",
            "value": json.dumps(payment.dict())
        }).execute()
        return {"message": "Payment info updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# For Vercel deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)