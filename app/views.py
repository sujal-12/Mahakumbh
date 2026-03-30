from django.shortcuts import render

from .models import *
from .auth import authentication 
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from app import views
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def shopkeeper_register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        shop_name = request.POST.get('shop_name')
        location = request.POST.get('shop_location')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        shop_image = request.FILES.get('shop_image')  # 🔥 image 

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('shopkeeper_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('shopkeeper_register.html')

        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
        user.save()
        
        shopkeeper_details = Shopkeeper.objects.create(
            user=user,
            first_name=fname,
            last_name=lname,
            mobile=mobile,
            shop_name=shop_name,
            location=location,
            username=username,
            shop_image=shop_image
        )
        
        shopkeeper_details.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('log_in')
    return render(request, 'shopkeeper_register.html')

def visitor_register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')  # 🔥 new field
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('visitor_register')

        if Visitor.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('visitor_register')

        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)
        user.save() 
        
        
        Visitor.objects.create(
            first_name=fname,
            last_name=lname,
            mobile=mobile,
            username=username,
            address=address
        )

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('log_in')

    return render(request, 'visitor_register.html')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin@gmail.com' and password == 'admin@123':
            admin_user, created = User.objects.get_or_create(username='admin@gmail.com', email='admin@gmail.com')
            admin_user.set_password('admin@123')
            admin_user.save()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Log In Successful...!")
                return redirect("admin_dashboard.html")
            else:
                messages.error(request, "Invalid User...!")
                return redirect("admin_login.html")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("admin_login.html")

    return render(request, "admin_login.html", {'action': 'admin_login'})


def admin_dashboard(request):
    visitors = Visitor.objects.all()
    shopkeepers = Shopkeeper.objects.all()
    all_user = User.objects.all()
    crowd_data = CrowdDetection.objects.all().order_by('detected_at')
    
    
    context = {
        'visitors' : visitors,
        'shopkeepers': shopkeepers,
        'all_user':all_user,
        'crowd_data': crowd_data
    }
    return render(request, "admin_dashboard.html", context)


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")

            # Check if user is Shopkeeper
            if Shopkeeper.objects.filter(username=username).exists():
                return redirect("shopkeeper_dashboard.html")  # URL name for shopkeeper dashboard

            # Check if user is Visitor
            elif Visitor.objects.filter(username=username).exists():
                return redirect("dashboard.html")  # URL name for visitor dashboard

            else:
                # Default fallback
                return redirect("dashboard")

        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect("log_in")

    return render(request, "log_in.html")


def visitor_dashboard(request):
    return render(request, "visitor_dashboard.html")

from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def shopkeeper_dashboard(request):

    shopkeeper = Shopkeeper.objects.get(user=request.user)
    

    if request.method == "POST":
        product_names = request.POST.getlist("product_name[]")
        product_prices = request.POST.getlist("product_price[]")
        product_quantities = request.POST.getlist("product_quantity[]")  # ✅ NEW

        added = False   # flag

        for name, price in zip(product_names, product_prices):
            if name and price:
                Product.objects.create(
                    shopkeeper=shopkeeper,
                    product_name=name,
                    product_price=price,
                    quantity=product_quantities[product_names.index(name)] if product_names.index(name) < len(product_quantities) else 1,
                )
                added = True

        if added:
            messages.success(request, "Product added successfully ✅")
            return redirect("shopkeeper_dashboard.html")  # page reload to avoid duplicate submit

    products = Product.objects.filter(shopkeeper=shopkeeper)
    feedback = Feedback.objects.filter(shopkeeper=shopkeeper).select_related('visitor').order_by('-created_at')
    purchase_order = Purchase.objects.filter(shopkeeper=shopkeeper).select_related('visitor', 'product').order_by('-purchased_at')

    return render(request, "shopkeeper_dashboard.html", {
        "shopkeeper": shopkeeper,   # ✅ add this line
        "products": products,
        "feedback": feedback,
        "purchase_order": purchase_order
    })

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Shopkeeper, Product, Purchase


from decimal import Decimal

from decimal import Decimal

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Shopkeeper, Product, Purchase, Visitor

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Shopkeeper, Product, Purchase, Visitor, Feedback

from django.shortcuts import render, redirect
from decimal import Decimal
from .models import Shopkeeper, Visitor, Product, Purchase, Feedback

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shopkeeper, Product, Purchase, Visitor, Feedback

from decimal import Decimal
from django.shortcuts import render, redirect
from .models import Shopkeeper, Product, Purchase, Visitor, Feedback

def dashboard(request):

    if request.method == "POST":
        # Purchase Submit
        if "purchase_submit" in request.POST:
            shop_id = request.POST.get("shop_id")
            try:
                shop = Shopkeeper.objects.get(id=shop_id)
                if request.user.is_authenticated:
                    visitor = Visitor.objects.get(username=request.user.username)
                    product_ids = request.POST.getlist("product_id[]")

                    for pid in product_ids:
                        qty_str = request.POST.get(f"buy_qty_{pid}", "0")
                        qty = int(qty_str) if qty_str.isdigit() else 0

                        if qty > 0:
                            product = Product.objects.get(id=pid)
                            if product.quantity >= qty:
                                total = Decimal(product.product_price) * qty
                                Purchase.objects.create(
                                    visitor=visitor,
                                    shopkeeper=shop,
                                    product=product,
                                    quantity=qty,
                                    total_price=total
                                )
                                product.quantity -= qty
                                product.save()
            except:
                pass
            return redirect("dashboard.html")

        # Feedback Submit
        elif "feedback_submit" in request.POST:
            shop_id = request.POST.get("shop_id")
            try:
                shop = Shopkeeper.objects.get(id=shop_id)
                if request.user.is_authenticated:
                    visitor = Visitor.objects.get(username=request.user.username)
                    comment = request.POST.get("feedback", "").strip()
                    rating = int(request.POST.get("rating", 0))

                    if comment or rating > 0:
                        Feedback.objects.create(
                            visitor=visitor,
                            shopkeeper=shop,
                            comment=comment,
                            rating=rating
                        )
            except:
                pass
            return redirect("dashboard.html")

    # ====================== GET Request ======================
    shops_data = Shopkeeper.objects.prefetch_related('product_set').all()

    purchases = Purchase.objects.none()
    nearby_shops = Shopkeeper.objects.none()

    if request.user.is_authenticated:
        try:
            visitor = Visitor.objects.get(username=request.user.username)
            
            # Purchase History
            purchases = Purchase.objects.filter(visitor=visitor)\
                        .select_related('shopkeeper', 'product')\
                        .order_by('-purchased_at')

            # ==================== NEARBY SHOPS LOGIC ====================
            if visitor.address:
                visitor_loc = visitor.address.strip().lower()

                # Primary: Exact or partial match
                nearby_shops = Shopkeeper.objects.filter(
                    location__icontains=visitor_loc
                )

                # Fallback 1: First meaningful word
                if not nearby_shops.exists():
                    first_word = visitor_loc.split()[0] if visitor_loc.split() else ""
                    if first_word and len(first_word) > 3:
                        nearby_shops = Shopkeeper.objects.filter(
                            location__icontains=first_word
                        )

                # Fallback 2: Any keyword match
                if not nearby_shops.exists():
                    for word in visitor_loc.split():
                        if len(word) > 3:
                            nearby_shops = Shopkeeper.objects.filter(
                                location__icontains=word
                            )
                            if nearby_shops.exists():
                                break

        except Visitor.DoesNotExist:
            pass

    context = {
        'shops_data': shops_data,
        'purchases': purchases,
        'nearby_shops': nearby_shops,
        'crowd_percentage': request.session.pop('crowd_percentage', None),
    }

    return render(request, "dashboard.html", context)


def shop_products(request, shop_id):
    shop = get_object_or_404(Shopkeeper, id=shop_id)
    products = Product.objects.filter(shopkeeper=shop)

    return render(request, "shop_products.html", {
        "shop": shop,
        "products": products
    })
    
    
def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("/")




from django.shortcuts import redirect
import cv2
import numpy as np

# YOLO setup (paths should be updated)
weights_path = "app/OverCrowdDetection/yolov3.weights"
config_path = "app/OverCrowdDetection/yolov3.cfg"
names_path = "app/OverCrowdDetection/coco.names"

# Load classes
with open(names_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers().flatten()]
color = (0, 255, 0)

def open_camera(request):
    cap = cv2.VideoCapture(0)
    max_persons = 10  # define max number of persons for 100%
    crowd_percentage = 0  # default

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, channels = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416,416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids, confidences, boxes = [], [], []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if classes[class_id] == "person" and confidence > 0.5:
                    cx = int(detection[0] * width)
                    cy = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(cx - w/2)
                    y = int(cy - h/2)
                    boxes.append([x,y,w,h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        person_count = len(indexes)

        # Compute percentage (10% per person, max 100%)
        crowd_percentage = min(person_count * 10, 100)

        # Draw boxes & overlay
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                cv2.putText(frame, "Person", (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Display percentage live
        cv2.putText(frame, f"Crowd: {crowd_percentage}%", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
        if crowd_percentage > 30:
            cv2.putText(frame, "OVERCROWDED!", (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

        cv2.imshow("People Detection (YOLOv3)", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    # Save in database
    crowed = CrowdDetection.objects.create(
        location_name="Location 1",
        people_count=person_count,
        crowd_percentage=crowd_percentage
    )
    
    crowed.save()
    
    

    # Save the last percentage in session
    request.session['crowd_percentage'] = crowd_percentage

    # Redirect to dashboard
    return redirect('dashboard.html')
