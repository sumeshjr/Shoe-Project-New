from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import *
from django.http import Http404
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone


# Use the get_user_model function to get the custom user model
User = get_user_model()

def index(request):
    sizes = [5, 6, 7, 8, 9, 10, 11, 12]
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products,'sizes': sizes})

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

# Admin Dashboard
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'admin/admin_dashboard.html',{'products':products})



def approve_user(request, user_id):

    user = get_object_or_404(User, id=user_id)

    # Check if the user is already approved
    if user.is_approved:
        messages.info(request, f"User {user.username} is already approved.")
    else:
        # Approve the user
        user.is_approved = True
        user.save()
        messages.success(request, f"User {user.username} has been approved.")
    
    return redirect('admin_dashboard')

def approve_supplier(request, supplier_id):
    # Ensure that the logged-in user is an admin
    supplier = get_object_or_404(Supplier, id=supplier_id)
    
    # Check if the supplier is already approved
    if supplier.user.is_approved:
        messages.info(request, f"Supplier {supplier.company_name} is already approved.")
    else:
        # Approve the supplier
        supplier.user.is_approved = True
        supplier.user.save()
        messages.success(request, f"Supplier {supplier.company_name} has been approved.")
    
    return redirect('admin_dashboard')

def view_all_users(request):
    # Fetch all users who are not superusers and whose role is not 'supplier'
    users = User.objects.filter(is_superuser=False).exclude(role='supplier')
    
    # Render the template and pass the filtered list of users
    return render(request, 'admin/view_all_users.html', {'users': users})


def view_all_suppliers(request):
    # Fetch all suppliers
    suppliers = Supplier.objects.all()
    
    # Render the template and pass the list of suppliers
    return render(request, 'admin/view_all_suppliers.html', {'suppliers': suppliers})

def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_role = request.POST.get('role')

        # Validate the inputs (basic validation for example)
        if new_username and new_email and new_role in ['admin', 'supplier', 'user']:
            user.username = new_username
            user.email = new_email
            user.role = new_role
            user.save()
            messages.success(request, f'User {user.username} updated successfully.')
        else:
            messages.error(request, 'Invalid input.')

        return redirect('view_all_users')  # Redirect to the page showing all users

    return render(request, 'admin/update_user.html', {'user': user})

def update_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        new_company_name = request.POST.get('company_name')
        new_contact_info = request.POST.get('contact_info')

        if new_company_name:
            supplier.company_name = new_company_name
        if new_contact_info:
            supplier.contact_info = new_contact_info

        supplier.save()
        messages.success(request, f'Supplier {supplier.company_name} updated successfully.')

        return redirect('view_all_suppliers')  # Redirect to the page showing all suppliers

    return render(request, 'admin/update_supplier.html', {'supplier': supplier})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':  # Ensure deletion is a POST request
        user.delete()
        messages.success(request, f'User {user.username} deleted successfully.')
        return redirect('view_all_users')  # Redirect to the page showing all users

    return render(request, 'admin/delete_user.html', {'user': user})

def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':  # Ensure deletion is a POST request
        supplier.delete()
        messages.success(request, f'Supplier {supplier.company_name} deleted successfully.')
        return redirect('view_all_suppliers')  # Redirect to the page showing all suppliers

    return render(request, 'admin/delete_supplier.html', {'supplier': supplier})

#______________________________________________________________________________________________________________#

# Supplier Dashboard
def supplier_dashboard(request):
    return render(request, 'supplier/supplier_dashboard.html')

#______________________________________________________________________________________________________________#

# User Dashboard
def user_dashboard(request):
    products = Product.objects.all()
    sizes = [5, 6, 7, 8, 9, 10, 11, 12]  # Define size options here
    return render(request, 'user/user_dashboard.html',{'products': products, 'sizes': sizes})

def view_profile(request):
    # Get the current user's details
    user = request.user

    # Render the profile page with user details
    return render(request, 'user/view_profile.html', {'user': user})

def supplier_profile(request):
    # Get the current user's details
    user = request.user

    # Render the profile page with user details
    return render(request, 'supplier/view_profile.html', {'user': user})

def update_supplier_profile(request):
    # Get the current user's details
    user = request.user

    if request.method == 'POST':
        # Get the updated data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Update user attributes
        user.username = username
        user.email = email
        user.save()

        # Show a success message
        messages.success(request, "Profile updated successfully!")
        return redirect('update_profile')  # Redirect to the same page after update

    return render(request, 'supplier/update_profile.html', {'user': user})


def update_profile(request):
    # Get the current user's details
    user = request.user

    if request.method == 'POST':
        # Get the updated data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        # Update user attributes
        user.username = username
        user.email = email
        user.save()

        # Show a success message
        messages.success(request, "Profile updated successfully!")
        return redirect('update_profile')  # Redirect to the same page after update

    return render(request, 'user/update_profile.html', {'user': user})

def add_to_cart(request):
    if request.method == 'POST':
        # Get the product id and size from the form submission
        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        
        # Get the product object based on the provided product_id
        product = get_object_or_404(Product, id=product_id)

        # Get or create the user's cart (assuming the user is logged in)
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product with the selected size already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': 1}  # Add 1 item if the cart item is new
        )

        if not created:
            # If the cart item already exists, just increment the quantity
            cart_item.quantity += 1
            cart_item.save()

        # Redirect to the cart page or any page you prefer after adding to cart
        return redirect('view_cart')  # Replace 'cart' with your actual cart URL name if needed

    # If the method is not POST, just redirect to the home or products page
    return redirect('home') 


def remove_from_cart(request):
    if request.method == 'POST':
        # Get the product ID from the form submission
        product_id = request.POST.get('product_id')

        # Get the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Find the cart item and delete it
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if cart_item:
            cart_item.delete()

        # Redirect back to the cart page
        return redirect('view_cart')

    return redirect('home')

def view_cart(request):
    # Get the user's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    # If the cart exists, fetch the cart items
    if cart:
        cart_items = cart.cart_items.all()
    else:
        cart_items = []

    # Render the cart page with the cart items
    return render(request, 'user/cart.html', {'cart_items': cart_items})

def view_categories(request):
    categories = ProductCategory.objects.all()  # Fetch all categories
    return render(request, 'user/categories.html', {'categories': categories})

def view_products_by_category(request, category_id):
    sizes = [5, 6, 7, 8, 9, 10, 11, 12] 
    category = get_object_or_404(ProductCategory, id=category_id)  # Get the category
    products = Product.objects.filter(category=category)  # Get products by category
    return render(request, 'user/products_by_category.html', {'category': category, 'products': products,'sizes':sizes})

def search_view(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request

    # Initialize empty result sets
    products = Product.objects.none()
    sizes = [5, 6, 7, 8, 9, 10, 11, 12] 

    if query:
        # Search for products by name or description
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
       
    return render(request, 'user/search_results.html', {'products': products, 'query': query,'sizes':sizes})

#______________________________________________________________________________________________________________#
# Register Supplier
def register_supplier(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # Get confirm password field
        company_name = request.POST.get('company_name')
        contact_info = request.POST.get('contact_info')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_supplier')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_supplier')

        supplier_user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='supplier',
        )
        Supplier.objects.create(user=supplier_user, company_name=company_name, contact_info=contact_info)
        messages.success(request, 'Supplier registered successfully!')
        return redirect('login')

    return render(request, 'supplier/register_supplier.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # Get confirm password field

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register_user')

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role='user',
            is_approved=True
        )
        messages.success(request, 'User registered successfully!')
        return redirect('login')

    return render(request, 'user/register_user.html')

# Login for All Roles
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the custom User model
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                    return redirect('/admin_dashboard/')
            # Check if the user is approved
            elif user.is_approved:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Debugging output to check if user and role are correct
                print(f"User: {user}, Role: {user.role}")

                # Redirect based on the user's role
                if user.role == 'supplier':
                    return redirect('/supplier_dashboard/')
                elif user.role == 'user':
                    return redirect('/user_dashboard/')
                else:
                    messages.error(request, 'Invalid role assigned to the user.')
                    return redirect('login')
            else:
                messages.error(request, 'Your account is not approved yet. Please contact the admin.')
                return redirect('login')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

#___________________________________________________________________________________________________
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description', '')

        if category_name:
            try:

                # Create the new category for the logged-in supplier
                ProductCategory.objects.create(
                    name=category_name,
                    description=category_description,
                )
                messages.success(request, 'Category added successfully!')
                return redirect('view_all_categories')  # Redirect to the page displaying all categories
            except Supplier.DoesNotExist:
                # Handle the case where the user is not associated with a supplier
                messages.error(request, 'You must be a supplier to add categories.')
                return redirect('supplier_dashboard')  # Redirect to the supplier dashboard or another appropriate page
        else:
            messages.error(request, 'Category name is required!')

    return render(request, 'admin/add_category.html')

# Update Category for Supplier
def update_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('category_name', category.name)
        category.description = request.POST.get('category_description', category.description)
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('view_all_categories')  # Redirect to the page displaying all categories
    return render(request, 'admin/update_category.html', {'category': category})

# Delete Category for Supplier
def delete_category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('view_all_categories')  # Redirect to the page displaying all categories

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_category_id = request.POST.get('category')
        product_description = request.POST.get('description', '')
        product_price = request.POST.get('price')
        product_stock = request.POST.get('stock')
        product_image = request.FILES.get('image')  # Handle image upload

        if product_name and product_price and product_stock:
            category = get_object_or_404(ProductCategory, id=product_category_id)
            Product.objects.create(
                name=product_name,
                category=category,
                description=product_description,
                price=product_price,
                stock=product_stock,
                image_url=product_image,  # Save the uploaded image
            )
            messages.success(request, 'Product added successfully!')
            return redirect('view_all_products')  # Redirect to the page displaying all products
        else:
            messages.error(request, 'Product name, price, and stock are required!')

    categories = ProductCategory.objects.all()
    return render(request, 'admin/add_product.html', {'categories': categories})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('product_name', product.name)
        product.category = get_object_or_404(ProductCategory, id=request.POST.get('category', product.category.id))
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)

        # Handle image update
        if 'image' in request.FILES:  # Check if a new image was uploaded
            product.image_url = request.FILES['image']

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('view_all_products')  # Redirect to the page displaying all products

    categories = ProductCategory.objects.all()
    return render(request, 'admin/update_product.html', {'product': product, 'categories': categories})

# Delete Product for Supplier
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('view_all_products')  # Redirect to the page displaying all products

def view_all_categories(request):
    # Filter categories by the logged-in supplier
    categories = ProductCategory.objects.all()
    return render(request, 'admin/view_all_categories.html', {'categories': categories})

# View all products added by the supplier
def view_all_products(request):

    products = Product.objects.all()
    return render(request, 'admin/view_all_products.html', {'products': products})


def view_products(request):
    products = Product.objects.all()
    return render(request, 'supplier/view_products.html', {'products': products})


def user_logout(request):
    # Log the user out
    logout(request)
    # Redirect to a page after logging out (usually a login page or home page)
    return redirect('index')


def list_update_requests(request):
    update_requests = ProductUpdateRequest.objects.all().order_by('-requested_at')
    return render(request, 'admin/update_list.html', {'update_requests': update_requests})

def create_update_request(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    supplier = get_object_or_404(Supplier, user=request.user)

    # Check if a pending request already exists
    existing_request = ProductUpdateRequest.objects.filter(product=product, supplier=supplier, is_approved=False)
    dup_req = ProductUpdateRequest.objects.filter(product=product, supplier=supplier, is_approved=True)
    if existing_request.exists():
        messages.warning(request, "An update request for this product is already pending.")
        return redirect('view_products')

    if dup_req.exists():
        messages.warning(request, "You already got update access.")
        return redirect('view_products')
    
    # Create the request
    ProductUpdateRequest.objects.create(product=product, supplier=supplier)
    messages.success(request, "Product update request submitted successfully.")
    return redirect('view_products')


def approve_update_request(request, request_id):
    update_request = get_object_or_404(ProductUpdateRequest, id=request_id)
    update_request.is_approved = True
    update_request.approved_at = timezone.now()
    update_request.save()

    messages.success(request, f"Update request for '{update_request.product.name}' approved.")
    return redirect('list_update_requests')

def update_product_supplier(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    supplier = get_object_or_404(Supplier, user=request.user)

    # 🔒 Check if there’s an approved update request for this product by the supplier
    approved_request_exists = ProductUpdateRequest.objects.filter(
        product=product, supplier=supplier, is_approved=True
    ).exists()

    if not approved_request_exists:
        messages.error(request, "You cannot update this product. An approved update request is required.")
        return redirect('view_products')

    if request.method == 'POST':
        product.name = request.POST.get('product_name', product.name)
        product.category = get_object_or_404(ProductCategory, id=request.POST.get('category', product.category.id))
        product.description = request.POST.get('description', product.description)
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)

        # Handle image update
        if 'image' in request.FILES:
            product.image_url = request.FILES['image']

        product.save()

        # 🚫 Optional: After update, remove the approved request so the supplier can't reuse it
        ProductUpdateRequest.objects.filter(product=product, supplier=supplier, is_approved=True).delete()

        messages.success(request, 'Product updated successfully!')
        return redirect('view_products')

    categories = ProductCategory.objects.all()
    return render(request, 'supplier/update_product.html', {'product': product, 'categories': categories})