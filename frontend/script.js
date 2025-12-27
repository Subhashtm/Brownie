// Global variables
let currentUser = null;
let cart = [];
let products = [];
let isAdmin = false;

// API base URL
const API_BASE = '';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    loadProducts();
    loadContactInfo();
    checkAuthStatus();
});

// Initialize app
function initializeApp() {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('userRole');
    
    if (token) {
        currentUser = { token, role: userRole };
        updateUIForLoggedInUser();
        if (userRole === 'admin') {
            isAdmin = true;
            document.getElementById('admin-btn').classList.remove('hidden');
        }
        loadCart();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    document.querySelector('.hamburger').addEventListener('click', toggleMobileMenu);
    
    // Modal controls
    setupModalControls();
    
    // Auth forms
    document.getElementById('login-form').addEventListener('submit', handleLogin);
    document.getElementById('register-form').addEventListener('submit', handleRegister);
    
    // Cart
    document.getElementById('cart-btn').addEventListener('click', showCart);
    document.getElementById('checkout-btn').addEventListener('click', showCheckout);
    
    // Admin
    document.getElementById('login-btn').addEventListener('click', showLoginModal);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('admin-btn').addEventListener('click', showAdminPanel);
    
    // Admin tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });
    
    // Admin forms
    document.getElementById('add-product-btn').addEventListener('click', showAddProductForm);
    document.getElementById('product-form').addEventListener('submit', handleProductSubmit);
    document.getElementById('contact-settings-form').addEventListener('submit', handleContactUpdate);
    document.getElementById('payment-settings-form').addEventListener('submit', handlePaymentUpdate);
    
    // Contact form
    document.getElementById('contact-form').addEventListener('submit', handleContactForm);
}

// Setup modal controls
function setupModalControls() {
    const modals = document.querySelectorAll('.modal');
    const closeButtons = document.querySelectorAll('.close');
    
    closeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.target.closest('.modal').style.display = 'none';
        });
    });
    
    window.addEventListener('click', (e) => {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Auth modal switches
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('login-modal').style.display = 'none';
        document.getElementById('register-modal').style.display = 'block';
    });
    
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        document.getElementById('register-modal').style.display = 'none';
        document.getElementById('login-modal').style.display = 'block';
    });
}

// Toggle mobile menu
function toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.classList.toggle('active');
}

// Scroll to products
function scrollToProducts() {
    document.getElementById('products').scrollIntoView({ behavior: 'smooth' });
}

// API calls
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE}/api${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (currentUser && currentUser.token) {
        config.headers.Authorization = `Bearer ${currentUser.token}`;
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

// Authentication
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await apiCall('/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        localStorage.setItem('token', response.access_token);
        localStorage.setItem('userRole', response.role);
        
        currentUser = { token: response.access_token, role: response.role };
        
        if (response.role === 'admin') {
            isAdmin = true;
            document.getElementById('admin-btn').classList.remove('hidden');
        }
        
        updateUIForLoggedInUser();
        document.getElementById('login-modal').style.display = 'none';
        loadCart();
        
        showNotification('Login successful!', 'success');
    } catch (error) {
        showNotification('Login failed. Please check your credentials.', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        await apiCall('/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        
        document.getElementById('register-modal').style.display = 'none';
        showNotification('Registration successful! Please login.', 'success');
        showLoginModal();
    } catch (error) {
        showNotification('Registration failed. Please try again.', 'error');
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    currentUser = null;
    isAdmin = false;
    cart = [];
    
    updateUIForLoggedOutUser();
    showNotification('Logged out successfully!', 'success');
}

function updateUIForLoggedInUser() {
    document.getElementById('login-btn').classList.add('hidden');
    document.getElementById('logout-btn').classList.remove('hidden');
}

function updateUIForLoggedOutUser() {
    document.getElementById('login-btn').classList.remove('hidden');
    document.getElementById('logout-btn').classList.add('hidden');
    document.getElementById('admin-btn').classList.add('hidden');
    updateCartCount();
}

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    if (token) {
        // Verify token is still valid
        apiCall('/products').catch(() => {
            handleLogout();
        });
    }
}

// Products
async function loadProducts() {
    try {
        products = await apiCall('/products');
        displayProducts(products);
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function displayProducts(productsToShow) {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = '';
    
    productsToShow.forEach(product => {
        const productCard = createProductCard(product);
        grid.appendChild(productCard);
    });
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    
    const imageUrl = product.image_url || 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80';
    
    card.innerHTML = `
        <img src="${imageUrl}" alt="${product.name}" class="product-image">
        <div class="product-info">
            <h3 class="product-name">${product.name}</h3>
            <p class="product-description">${product.description}</p>
            <div class="product-price">₹${product.price.toFixed(2)}</div>
            <button class="add-to-cart-btn" onclick="addToCart(${product.id})">
                Add to Cart
            </button>
        </div>
    `;
    
    return card;
}

// Cart functionality
async function addToCart(productId) {
    if (!currentUser) {
        showNotification('Please login to add items to cart', 'error');
        showLoginModal();
        return;
    }
    
    try {
        await apiCall('/cart/add', {
            method: 'POST',
            body: JSON.stringify({ product_id: productId, quantity: 1 })
        });
        
        loadCart();
        showNotification('Item added to cart!', 'success');
    } catch (error) {
        showNotification('Failed to add item to cart', 'error');
    }
}

async function loadCart() {
    if (!currentUser) return;
    
    try {
        cart = await apiCall('/cart');
        updateCartCount();
    } catch (error) {
        console.error('Failed to load cart:', error);
    }
}

function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    document.getElementById('cart-count').textContent = count;
}

async function showCart() {
    if (!currentUser) {
        showNotification('Please login to view cart', 'error');
        showLoginModal();
        return;
    }
    
    await loadCart();
    displayCartItems();
    document.getElementById('cart-modal').style.display = 'block';
}

function displayCartItems() {
    const cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = '';
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty</p>';
        document.getElementById('cart-total').textContent = '0.00';
        return;
    }
    
    let total = 0;
    
    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        
        const itemTotal = item.products.price * item.quantity;
        total += itemTotal;
        
        cartItem.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${item.products.name}</div>
                <div class="cart-item-price">₹${item.products.price.toFixed(2)} each</div>
            </div>
            <div class="cart-item-actions">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, ${item.quantity - 1})">-</button>
                    <span>${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <button class="remove-btn" onclick="removeFromCart(${item.id})">Remove</button>
            </div>
        `;
        
        cartItemsContainer.appendChild(cartItem);
    });
    
    document.getElementById('cart-total').textContent = total.toFixed(2);
}

async function updateCartQuantity(itemId, newQuantity) {
    if (newQuantity <= 0) {
        removeFromCart(itemId);
        return;
    }
    
    // This would require an update cart endpoint
    // For now, we'll remove and re-add
    await removeFromCart(itemId);
    // Add logic to re-add with new quantity
}

async function removeFromCart(itemId) {
    try {
        await apiCall(`/cart/${itemId}`, { method: 'DELETE' });
        loadCart();
        displayCartItems();
        showNotification('Item removed from cart', 'success');
    } catch (error) {
        showNotification('Failed to remove item', 'error');
    }
}

// Checkout
async function showCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty', 'error');
        return;
    }
    
    try {
        const paymentInfo = await apiCall('/payment-info');
        
        document.getElementById('payment-qr-img').src = paymentInfo.qr_code_url || 'https://via.placeholder.com/200x200?text=QR+Code';
        document.getElementById('payment-email').textContent = paymentInfo.payment_email;
        
        document.getElementById('cart-modal').style.display = 'none';
        document.getElementById('checkout-modal').style.display = 'block';
    } catch (error) {
        showNotification('Failed to load payment information', 'error');
    }
}

// Contact
async function loadContactInfo() {
    try {
        const contactInfo = await apiCall('/contact');
        displayContactInfo(contactInfo);
    } catch (error) {
        console.error('Failed to load contact info:', error);
    }
}

function displayContactInfo(contactInfo) {
    const container = document.getElementById('contact-info');
    container.innerHTML = `
        <h3>Get in Touch</h3>
        <p><i class="fas fa-envelope"></i> ${contactInfo.email}</p>
        <p><i class="fas fa-phone"></i> ${contactInfo.phone}</p>
        <p><i class="fas fa-map-marker-alt"></i> ${contactInfo.address}</p>
    `;
}

async function handleContactForm(e) {
    e.preventDefault();
    showNotification('Thank you for your message! We will get back to you soon.', 'success');
    e.target.reset();
}

// Admin Panel
function showAdminPanel() {
    if (!isAdmin) {
        showNotification('Admin access required', 'error');
        return;
    }
    
    loadAdminProducts();
    loadAdminSettings();
    document.getElementById('admin-modal').style.display = 'block';
}

function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

async function loadAdminProducts() {
    try {
        const allProducts = await apiCall('/products');
        displayAdminProducts(allProducts);
    } catch (error) {
        console.error('Failed to load admin products:', error);
    }
}

function displayAdminProducts(products) {
    const container = document.getElementById('admin-products-list');
    container.innerHTML = '';
    
    products.forEach(product => {
        const productItem = document.createElement('div');
        productItem.className = 'admin-product-item';
        
        productItem.innerHTML = `
            <div class="admin-product-info">
                <h4>${product.name}</h4>
                <p>₹${product.price.toFixed(2)} - ${product.available ? 'Available' : 'Unavailable'}</p>
            </div>
            <div class="admin-product-actions">
                <button class="edit-btn" onclick="editProduct(${product.id})">Edit</button>
                <button class="delete-btn" onclick="deleteProduct(${product.id})">Delete</button>
            </div>
        `;
        
        container.appendChild(productItem);
    });
}

function showAddProductForm() {
    document.getElementById('product-form-title').textContent = 'Add Product';
    document.getElementById('product-form').reset();
    document.getElementById('product-id').value = '';
    document.getElementById('product-form-modal').style.display = 'block';
}

async function editProduct(productId) {
    try {
        const product = await apiCall(`/products/${productId}`);
        
        document.getElementById('product-form-title').textContent = 'Edit Product';
        document.getElementById('product-id').value = product.id;
        document.getElementById('product-name').value = product.name;
        document.getElementById('product-description').value = product.description;
        document.getElementById('product-price').value = product.price;
        document.getElementById('product-category').value = product.category;
        document.getElementById('product-available').checked = product.available;
        
        document.getElementById('product-form-modal').style.display = 'block';
    } catch (error) {
        showNotification('Failed to load product details', 'error');
    }
}

async function handleProductSubmit(e) {
    e.preventDefault();
    
    const productId = document.getElementById('product-id').value;
    
    const productData = {
        name: document.getElementById('product-name').value,
        description: document.getElementById('product-description').value,
        price: parseFloat(document.getElementById('product-price').value),
        category: document.getElementById('product-category').value,
        available: document.getElementById('product-available').checked
    };
    
    try {
        // Handle image upload if file is selected
        const imageFile = document.getElementById('product-image').files[0];
        if (imageFile) {
            const imageFormData = new FormData();
            imageFormData.append('file', imageFile);
            
            const imageResponse = await fetch('/api/admin/upload-image', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${currentUser.token}`
                },
                body: imageFormData
            });
            
            if (imageResponse.ok) {
                const imageData = await imageResponse.json();
                productData.image_url = imageData.image_url;
            } else {
                const errorData = await imageResponse.json();
                throw new Error(errorData.detail || 'Image upload failed');
            }
        }
        
        let response;
        if (productId) {
            // Update existing product
            response = await apiCall(`/admin/products/${productId}`, {
                method: 'PUT',
                body: JSON.stringify(productData)
            });
        } else {
            // Create new product
            response = await apiCall('/admin/products', {
                method: 'POST',
                body: JSON.stringify(productData)
            });
        }
        
        document.getElementById('product-form-modal').style.display = 'none';
        loadAdminProducts();
        loadProducts(); // Refresh main products display
        showNotification('Product saved successfully!', 'success');
    } catch (error) {
        showNotification(`Failed to save product: ${error.message}`, 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    
    try {
        await apiCall(`/admin/products/${productId}`, { method: 'DELETE' });
        loadAdminProducts();
        loadProducts(); // Refresh main products display
        showNotification('Product deleted successfully!', 'success');
    } catch (error) {
        showNotification('Failed to delete product', 'error');
    }
}

async function loadAdminSettings() {
    try {
        const [contactInfo, paymentInfo] = await Promise.all([
            apiCall('/contact'),
            apiCall('/payment-info')
        ]);
        
        // Populate contact form
        document.getElementById('contact-email').value = contactInfo.email;
        document.getElementById('contact-phone').value = contactInfo.phone;
        document.getElementById('contact-address').value = contactInfo.address;
        
        // Populate payment form
        document.getElementById('payment-qr-url').value = paymentInfo.qr_code_url;
        document.getElementById('payment-email-setting').value = paymentInfo.payment_email;
    } catch (error) {
        console.error('Failed to load admin settings:', error);
    }
}

async function handleContactUpdate(e) {
    e.preventDefault();
    
    const contactData = {
        email: document.getElementById('contact-email').value,
        phone: document.getElementById('contact-phone').value,
        address: document.getElementById('contact-address').value
    };
    
    try {
        await apiCall('/admin/contact', {
            method: 'PUT',
            body: JSON.stringify(contactData)
        });
        
        loadContactInfo(); // Refresh contact display
        showNotification('Contact information updated!', 'success');
    } catch (error) {
        showNotification('Failed to update contact information', 'error');
    }
}

async function handlePaymentUpdate(e) {
    e.preventDefault();
    
    const paymentData = {
        qr_code_url: document.getElementById('payment-qr-url').value,
        payment_email: document.getElementById('payment-email-setting').value
    };
    
    try {
        await apiCall('/admin/payment-info', {
            method: 'PUT',
            body: JSON.stringify(paymentData)
        });
        
        showNotification('Payment information updated!', 'success');
    } catch (error) {
        showNotification('Failed to update payment information', 'error');
    }
}

// Utility functions
function showLoginModal() {
    document.getElementById('login-modal').style.display = 'block';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 20px',
        borderRadius: '5px',
        color: 'white',
        zIndex: '3000',
        fontSize: '14px',
        maxWidth: '300px',
        backgroundColor: type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'
    });
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}