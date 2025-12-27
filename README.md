# Sweet Brownies - Professional Brownie Shop Web App

A modern, responsive web application for a brownie shop built with FastAPI, Supabase, and Dropbox integration.

## Features

### Customer Features
- **Browse Products**: View all available brownies without login
- **User Authentication**: Register and login to place orders
- **Shopping Cart**: Add items to cart and manage quantities
- **Secure Checkout**: QR code payment system with receipt submission
- **Contact Page**: Get in touch with the shop

### Admin Features
- **Product Management**: Add, edit, delete, and manage product availability
- **Image Upload**: Upload product images via Dropbox integration
- **Settings Management**: Update contact information and payment details
- **Order Management**: View and manage customer orders

## Technology Stack

- **Backend**: FastAPI with Uvicorn server
- **Database**: Supabase (PostgreSQL)
- **File Storage**: Local file system with image optimization
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Authentication**: JWT tokens with bcrypt password hashing

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Supabase account and project

### 2. Installation

```bash
# Clone or download the project
cd brownie_shop

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key
SECRET_KEY=your_jwt_secret_key
ADMIN_EMAIL=admin@brownieshop.com
ADMIN_PASSWORD=admin123
```

### 4. Database Setup

1. Create a new Supabase project
2. Run the SQL commands from `database_setup.sql` in your Supabase SQL editor
3. This will create all necessary tables and sample data

### 5. Start the Server

```bash
# Using the startup script (recommended)
python start_server.py

# Or manually
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at `http://localhost:8000`

## Default Admin Credentials

- **Email**: admin@brownieshop.com
- **Password**: admin123

**Important**: Change these credentials in production!

## Project Structure

```
brownie_shop/
├── backend/
│   └── main.py              # FastAPI application
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # CSS styles
│   └── script.js            # JavaScript functionality
├── uploads/                 # Image upload directory (created automatically)
├── requirements.txt         # Python dependencies
├── database_setup.sql       # Database schema and sample data
├── start_server.py         # Server startup script
├── .env.example            # Environment variables template
└── README.md               # This file
```

## API Endpoints

### Public Endpoints
- `GET /` - Main application
- `GET /api/products` - List all available products
- `GET /api/contact` - Get contact information
- `GET /api/payment-info` - Get payment information
- `POST /api/register` - User registration
- `POST /api/login` - User login

### Authenticated Endpoints
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `DELETE /api/cart/{item_id}` - Remove item from cart

### Admin Endpoints
- `POST /api/admin/products` - Create product
- `PUT /api/admin/products/{id}` - Update product
- `DELETE /api/admin/products/{id}` - Delete product
- `POST /api/admin/upload-image` - Upload product image
- `PUT /api/admin/contact` - Update contact information
- `PUT /api/admin/payment-info` - Update payment information

## Database Schema

### Tables
- **users**: Customer accounts
- **products**: Brownie products
- **cart**: Shopping cart items
- **orders**: Customer orders
- **order_items**: Order line items
- **settings**: Admin configuration settings

## Security Features

- JWT token authentication
- Bcrypt password hashing
- Admin-only endpoints protection
- CORS middleware configuration
- Input validation with Pydantic models

## Customization

### Adding New Product Categories
1. Update the `category` options in the admin panel
2. Modify the product form in `frontend/script.js`
3. Update the database enum if needed

### Styling Customization
- Modify `frontend/styles.css` for visual changes
- Update color scheme by changing CSS custom properties
- Responsive design breakpoints can be adjusted

### Payment Integration
- Currently uses QR code system
- Can be extended to integrate with payment gateways
- Payment verification logic can be added to order processing

## Deployment

### Production Considerations
1. Change default admin credentials
2. Use strong JWT secret key
3. Enable HTTPS
4. Configure proper CORS origins
5. Set up proper logging
6. Use environment-specific configurations

### Hosting Options
- **Backend**: Deploy on platforms like Heroku, Railway, or DigitalOcean
- **Database**: Supabase handles hosting
- **Static Files**: Can be served via CDN

## Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database connection issues**
   - Verify Supabase URL and keys in `.env`
   - Check if database tables are created

3. **Image upload failures**
   - Check if `uploads/` directory exists (created automatically)
   - Verify file permissions for the uploads directory
   - Ensure uploaded files are valid image formats

4. **CORS errors**
   - Ensure frontend is served from the same domain
   - Update CORS settings in `main.py` if needed

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify environment configuration
3. Check server logs for detailed error messages

## License

This project is for educational and commercial use. Modify as needed for your requirements.