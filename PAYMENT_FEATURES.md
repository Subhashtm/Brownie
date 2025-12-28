# Payment System Features

## New Features Added

### 1. Email Authentication for Payment with Upload Option

- **Payment Receipt Upload**: Customers can now upload payment receipts directly through the checkout process
- **Email Notifications**: When a payment receipt is uploaded, an automatic email is sent to the admin with order details
- **Order Management**: Each payment upload is linked to a specific order for better tracking

### 2. Admin Company Name Management

- **Company Info Settings**: Admin can now edit company name and tagline through the admin panel
- **Dynamic Branding**: Company name and tagline are dynamically updated across the website
- **Settings Tab**: New company information section in admin settings

### 3. Fixed Contact Details Update Issue

- **Database Constraint Fix**: Fixed the duplicate key error when updating contact information
- **Proper Upsert**: Using proper upsert with conflict resolution for settings updates
- **Error Handling**: Better error handling for database operations

## How to Use

### For Customers:
1. Add items to cart and proceed to checkout
2. Scan the QR code to make payment
3. Upload payment receipt using the upload form
4. Add optional notes about the payment
5. Receive confirmation once admin approves the payment

### For Admins:
1. Access admin panel after logging in as admin
2. **Payment Uploads Tab**: View all uploaded payment receipts
3. **Company Settings**: Update company name and tagline
4. **Contact Settings**: Update contact information
5. **Payment Settings**: Update QR code and payment email

## Email Configuration

Add these environment variables to your `.env` file:

```env
# Email Configuration (for payment notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password_here
```

### Gmail Setup:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for this application
3. Use the App Password in the `SMTP_PASSWORD` field

## Database Changes

New table added:
- `payment_uploads`: Stores uploaded payment receipts with order linking
- Updated `settings` table with proper conflict resolution

## API Endpoints Added

- `POST /api/create-order`: Create a new order
- `POST /api/upload-payment-receipt/{order_id}`: Upload payment receipt
- `GET /api/admin/payment-uploads`: Get all payment uploads (admin)
- `PUT /api/admin/payment-uploads/{upload_id}/status`: Update payment status (admin)
- `GET /api/company-info`: Get company information
- `PUT /api/admin/company-info`: Update company information (admin)

## Features Overview

### Payment Flow:
1. Customer creates order during checkout
2. Customer uploads payment receipt with optional notes
3. Admin receives email notification with order details
4. Admin reviews and approves/rejects payment
5. Order status is automatically updated

### Admin Features:
- View all payment uploads with order details
- Approve/reject payments with admin notes
- Update company branding information
- Manage contact and payment settings
- Email notifications for new payment uploads

### Error Fixes:
- Fixed duplicate key constraint error in settings updates
- Proper error handling for file uploads
- Better validation for payment receipts