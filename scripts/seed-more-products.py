import boto3
from datetime import datetime
from decimal import Decimal
import uuid

# Initialize DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('ekart-products-dev')

# Comprehensive product catalog
products = [
    # Electronics - Laptops
    {
        "product_id": str(uuid.uuid4()),
        "title": "MacBook Pro 16-inch M3 Pro",
        "description": "Apple MacBook Pro with M3 Pro chip, 16-inch Liquid Retina XDR display, 18GB unified memory, 512GB SSD",
        "price": Decimal("2499.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Laptops",
        "brand": "Apple",
        "stock_quantity": 15,
        "rating": Decimal("4.9"),
        "review_count": 342,
        "seller_id": "seller-001",
        "is_active": True,
        "variants": [],
        "images": [
            {"image_id": str(uuid.uuid4()), "url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=MacBook+Pro", "alt_text": "MacBook Pro", "is_primary": True}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Dell XPS 15 9530",
        "description": "15.6-inch FHD+ InfinityEdge display, Intel Core i7-13700H, 16GB RAM, 512GB SSD, NVIDIA GeForce RTX 4050",
        "price": Decimal("1799.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Laptops",
        "brand": "Dell",
        "stock": 22,
        "rating": Decimal("4.7"),
        "review_count": 189,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/0066CC/FFFFFF/?text=Dell+XPS+15", "alt_text": "Dell XPS 15"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Lenovo ThinkPad X1 Carbon Gen 11",
        "description": "14-inch WUXGA IPS display, Intel Core i7-1355U, 16GB RAM, 512GB SSD, Windows 11 Pro",
        "price": Decimal("1649.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Laptops",
        "brand": "Lenovo",
        "stock": 18,
        "rating": Decimal("4.6"),
        "review_count": 156,
        "seller_id": "seller-002",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=ThinkPad+X1", "alt_text": "ThinkPad X1"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Electronics - Smartphones
    {
        "product_id": str(uuid.uuid4()),
        "title": "iPhone 15 Pro Max",
        "description": "6.7-inch Super Retina XDR display, A17 Pro chip, 256GB storage, Titanium design, USB-C",
        "price": Decimal("1199.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "brand": "Apple",
        "stock": 45,
        "rating": Decimal("4.8"),
        "review_count": 892,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/1C1C1E/FFFFFF/?text=iPhone+15+Pro", "alt_text": "iPhone 15 Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Samsung Galaxy S24 Ultra",
        "description": "6.8-inch Dynamic AMOLED 2X display, Snapdragon 8 Gen 3, 256GB storage, 200MP camera, S Pen included",
        "price": Decimal("1299.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "brand": "Samsung",
        "stock": 38,
        "rating": Decimal("4.7"),
        "review_count": 654,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Galaxy+S24", "alt_text": "Galaxy S24 Ultra"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Google Pixel 8 Pro",
        "description": "6.7-inch LTPO OLED display, Google Tensor G3, 128GB storage, Best-in-class AI features",
        "price": Decimal("999.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Smartphones",
        "brand": "Google",
        "stock": 29,
        "rating": Decimal("4.6"),
        "review_count": 423,
        "seller_id": "seller-002",
        "images": [
            {"url": "https://via.placeholder.com/400x400/4285F4/FFFFFF/?text=Pixel+8+Pro", "alt_text": "Pixel 8 Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Electronics - Headphones
    {
        "product_id": str(uuid.uuid4()),
        "title": "Sony WH-1000XM5 Wireless Headphones",
        "description": "Industry-leading noise cancellation, 30-hour battery life, Hi-Res Audio, Multipoint connection",
        "price": Decimal("399.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Audio",
        "brand": "Sony",
        "stock": 67,
        "rating": Decimal("4.8"),
        "review_count": 1234,
        "seller_id": "seller-003",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Sony+WH-1000XM5", "alt_text": "Sony WH-1000XM5"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "AirPods Pro (2nd generation)",
        "description": "Active Noise Cancellation, Transparency mode, Personalized Spatial Audio, MagSafe charging",
        "price": Decimal("249.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Audio",
        "brand": "Apple",
        "stock": 89,
        "rating": Decimal("4.7"),
        "review_count": 2156,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/FFFFFF/000000/?text=AirPods+Pro", "alt_text": "AirPods Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Bose QuietComfort Ultra Headphones",
        "description": "World-class noise cancellation, Spatial Audio, 24-hour battery, Premium comfort",
        "price": Decimal("429.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Audio",
        "brand": "Bose",
        "stock": 43,
        "rating": Decimal("4.6"),
        "review_count": 567,
        "seller_id": "seller-003",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Bose+QC+Ultra", "alt_text": "Bose QC Ultra"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Electronics - Smartwatches
    {
        "product_id": str(uuid.uuid4()),
        "title": "Apple Watch Series 9 GPS + Cellular 45mm",
        "description": "Always-On Retina display, S9 chip, Advanced health features, 18-hour battery, Crash Detection",
        "price": Decimal("499.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Wearables",
        "brand": "Apple",
        "stock": 56,
        "rating": Decimal("4.8"),
        "review_count": 987,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Apple+Watch+9", "alt_text": "Apple Watch Series 9"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Samsung Galaxy Watch 6 Classic 47mm",
        "description": "Rotating bezel, Advanced sleep tracking, Body composition analysis, Sapphire crystal display",
        "price": Decimal("429.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Wearables",
        "brand": "Samsung",
        "stock": 34,
        "rating": Decimal("4.6"),
        "review_count": 445,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/1C1C1E/FFFFFF/?text=Galaxy+Watch+6", "alt_text": "Galaxy Watch 6"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Electronics - Tablets
    {
        "product_id": str(uuid.uuid4()),
        "title": "iPad Pro 12.9-inch M2",
        "description": "12.9-inch Liquid Retina XDR display, M2 chip, 256GB storage, Apple Pencil support, 5G capable",
        "price": Decimal("1099.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Tablets",
        "brand": "Apple",
        "stock": 28,
        "rating": Decimal("4.9"),
        "review_count": 678,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/E5E5E7/000000/?text=iPad+Pro", "alt_text": "iPad Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Samsung Galaxy Tab S9 Ultra",
        "description": "14.6-inch Dynamic AMOLED 2X display, Snapdragon 8 Gen 2, 256GB storage, S Pen included",
        "price": Decimal("1199.99"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Tablets",
        "brand": "Samsung",
        "stock": 19,
        "rating": Decimal("4.7"),
        "review_count": 234,
        "seller_id": "seller-001",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Tab+S9+Ultra", "alt_text": "Tab S9 Ultra"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Home & Kitchen - Coffee Makers
    {
        "product_id": str(uuid.uuid4()),
        "title": "Breville Barista Express Espresso Machine",
        "description": "Built-in conical burr grinder, Microfoam milk texturing, PID temperature control, Stainless steel",
        "price": Decimal("699.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Coffee Makers",
        "brand": "Breville",
        "stock": 24,
        "rating": Decimal("4.7"),
        "review_count": 3421,
        "seller_id": "seller-004",
        "images": [
            {"url": "https://via.placeholder.com/400x400/8B4513/FFFFFF/?text=Breville+Barista", "alt_text": "Breville Barista"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Keurig K-Elite Coffee Maker",
        "description": "Strong brew setting, Iced coffee capability, 75oz reservoir, Programmable auto on/off",
        "price": Decimal("169.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Coffee Makers",
        "brand": "Keurig",
        "stock": 78,
        "rating": Decimal("4.5"),
        "review_count": 5632,
        "seller_id": "seller-004",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Keurig+K-Elite", "alt_text": "Keurig K-Elite"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Home & Kitchen - Air Fryers
    {
        "product_id": str(uuid.uuid4()),
        "title": "Ninja Air Fryer Max XL",
        "description": "5.5 quart capacity, Max Crisp Technology, 7 cooking functions, Dishwasher safe basket",
        "price": Decimal("129.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Air Fryers",
        "brand": "Ninja",
        "stock": 92,
        "rating": Decimal("4.8"),
        "review_count": 8934,
        "seller_id": "seller-004",
        "images": [
            {"url": "https://via.placeholder.com/400x400/FF0000/FFFFFF/?text=Ninja+Air+Fryer", "alt_text": "Ninja Air Fryer"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Philips Premium Airfryer XXL",
        "description": "7 quart capacity, Fat Removal technology, Smart sensing, Keep warm function, Digital touchscreen",
        "price": Decimal("349.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Air Fryers",
        "brand": "Philips",
        "stock": 41,
        "rating": Decimal("4.6"),
        "review_count": 2341,
        "seller_id": "seller-004",
        "images": [
            {"url": "https://via.placeholder.com/400x400/0066CC/FFFFFF/?text=Philips+Airfryer", "alt_text": "Philips Airfryer"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Home & Kitchen - Vacuum Cleaners
    {
        "product_id": str(uuid.uuid4()),
        "title": "Dyson V15 Detect Cordless Vacuum",
        "description": "Laser dust detection, LCD screen with real-time particle count, 60 minutes run time, HEPA filtration",
        "price": Decimal("749.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Vacuum Cleaners",
        "brand": "Dyson",
        "stock": 33,
        "rating": Decimal("4.7"),
        "review_count": 1567,
        "seller_id": "seller-005",
        "images": [
            {"url": "https://via.placeholder.com/400x400/6B46C1/FFFFFF/?text=Dyson+V15", "alt_text": "Dyson V15"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "iRobot Roomba j7+ Robot Vacuum",
        "description": "Advanced AI obstacle avoidance, Self-emptying base, Smart mapping, Voice control compatible",
        "price": Decimal("799.99"),
        "currency": "USD",
        "category": "Home & Kitchen",
        "subcategory": "Vacuum Cleaners",
        "brand": "iRobot",
        "stock": 47,
        "rating": Decimal("4.6"),
        "review_count": 2789,
        "seller_id": "seller-005",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Roomba+j7", "alt_text": "Roomba j7+"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Sports & Fitness - Smart Scales
    {
        "product_id": str(uuid.uuid4()),
        "title": "Withings Body+ Smart Scale",
        "description": "Full body composition analysis, WiFi & Bluetooth sync, Tracks 8 metrics, Multi-user recognition",
        "price": Decimal("99.99"),
        "currency": "USD",
        "category": "Sports & Fitness",
        "subcategory": "Smart Scales",
        "brand": "Withings",
        "stock": 125,
        "rating": Decimal("4.5"),
        "review_count": 3456,
        "seller_id": "seller-006",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Withings+Body", "alt_text": "Withings Body+"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Sports & Fitness - Fitness Trackers
    {
        "product_id": str(uuid.uuid4()),
        "title": "Fitbit Charge 6",
        "description": "Built-in GPS, Heart rate monitoring, Sleep tracking, 7-day battery life, Water resistant 50m",
        "price": Decimal("159.99"),
        "currency": "USD",
        "category": "Sports & Fitness",
        "subcategory": "Fitness Trackers",
        "brand": "Fitbit",
        "stock": 87,
        "rating": Decimal("4.4"),
        "review_count": 2134,
        "seller_id": "seller-006",
        "images": [
            {"url": "https://via.placeholder.com/400x400/00B0B9/FFFFFF/?text=Fitbit+Charge+6", "alt_text": "Fitbit Charge 6"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Garmin Forerunner 965",
        "description": "AMOLED display, Training readiness, Race predictor, 23-day battery, Full-color maps",
        "price": Decimal("599.99"),
        "currency": "USD",
        "category": "Sports & Fitness",
        "subcategory": "Fitness Trackers",
        "brand": "Garmin",
        "stock": 39,
        "rating": Decimal("4.8"),
        "review_count": 876,
        "seller_id": "seller-006",
        "images": [
            {"url": "https://via.placeholder.com/400x400/007CC3/FFFFFF/?text=Garmin+965", "alt_text": "Garmin Forerunner 965"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Sports & Fitness - Yoga Mats
    {
        "product_id": str(uuid.uuid4()),
        "title": "Manduka PRO Yoga Mat",
        "description": "6mm thick, Superior cushioning, Lifetime guarantee, Non-slip surface, Eco-friendly materials",
        "price": Decimal("119.99"),
        "currency": "USD",
        "category": "Sports & Fitness",
        "subcategory": "Yoga Equipment",
        "brand": "Manduka",
        "stock": 156,
        "rating": Decimal("4.7"),
        "review_count": 4567,
        "seller_id": "seller-006",
        "images": [
            {"url": "https://via.placeholder.com/400x400/6B46C1/FFFFFF/?text=Manduka+PRO", "alt_text": "Manduka PRO"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Books - Fiction
    {
        "product_id": str(uuid.uuid4()),
        "title": "Project Hail Mary by Andy Weir",
        "description": "Hardcover - A lone astronaut must save the Earth from disaster in this propulsive new sci-fi thriller",
        "price": Decimal("24.99"),
        "currency": "USD",
        "category": "Books",
        "subcategory": "Science Fiction",
        "brand": "Ballantine Books",
        "stock": 234,
        "rating": Decimal("4.9"),
        "review_count": 12456,
        "seller_id": "seller-007",
        "images": [
            {"url": "https://via.placeholder.com/400x600/8B4513/FFFFFF/?text=Project+Hail+Mary", "alt_text": "Project Hail Mary"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "The Midnight Library by Matt Haig",
        "description": "Between life and death, there's a library. A place where the books on the shelves represent possible lives.",
        "price": Decimal("16.99"),
        "currency": "USD",
        "category": "Books",
        "subcategory": "Contemporary Fiction",
        "brand": "Viking",
        "stock": 189,
        "rating": Decimal("4.6"),
        "review_count": 8934,
        "seller_id": "seller-007",
        "images": [
            {"url": "https://via.placeholder.com/400x600/1C1C1E/FFFFFF/?text=Midnight+Library", "alt_text": "The Midnight Library"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Gaming - Consoles
    {
        "product_id": str(uuid.uuid4()),
        "title": "PlayStation 5 Console",
        "description": "Ultra-high speed SSD, Ray tracing, 4K gaming, Tempest 3D AudioTech, DualSense wireless controller",
        "price": Decimal("499.99"),
        "currency": "USD",
        "category": "Gaming",
        "subcategory": "Consoles",
        "brand": "Sony",
        "stock": 12,
        "rating": Decimal("4.8"),
        "review_count": 5678,
        "seller_id": "seller-008",
        "images": [
            {"url": "https://via.placeholder.com/400x400/003791/FFFFFF/?text=PlayStation+5", "alt_text": "PlayStation 5"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Xbox Series X",
        "description": "12 teraflops GPU power, 4K gaming at 120 FPS, 1TB SSD, Quick Resume, Game Pass compatible",
        "price": Decimal("499.99"),
        "currency": "USD",
        "category": "Gaming",
        "subcategory": "Consoles",
        "brand": "Microsoft",
        "stock": 18,
        "rating": Decimal("4.7"),
        "review_count": 4321,
        "seller_id": "seller-008",
        "images": [
            {"url": "https://via.placeholder.com/400x400/107C10/FFFFFF/?text=Xbox+Series+X", "alt_text": "Xbox Series X"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Nintendo Switch OLED Model",
        "description": "7-inch OLED screen, Enhanced audio, 64GB storage, Adjustable stand, Handheld and docked modes",
        "price": Decimal("349.99"),
        "currency": "USD",
        "category": "Gaming",
        "subcategory": "Consoles",
        "brand": "Nintendo",
        "stock": 67,
        "rating": Decimal("4.8"),
        "review_count": 7890,
        "seller_id": "seller-008",
        "images": [
            {"url": "https://via.placeholder.com/400x400/E60012/FFFFFF/?text=Switch+OLED", "alt_text": "Switch OLED"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Gaming - Accessories
    {
        "product_id": str(uuid.uuid4()),
        "title": "Logitech G Pro X Superlight Gaming Mouse",
        "description": "63g ultra-lightweight, HERO 25K sensor, 70-hour battery, LIGHTSPEED wireless, Ambidextrous design",
        "price": Decimal("159.99"),
        "currency": "USD",
        "category": "Gaming",
        "subcategory": "Gaming Mice",
        "brand": "Logitech",
        "stock": 143,
        "rating": Decimal("4.8"),
        "review_count": 3421,
        "seller_id": "seller-009",
        "images": [
            {"url": "https://via.placeholder.com/400x400/00B8FC/FFFFFF/?text=G+Pro+Superlight", "alt_text": "G Pro Superlight"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Razer BlackWidow V4 Pro Mechanical Keyboard",
        "description": "Green mechanical switches, Programmable command dial, Underglow RGB, Magnetic wrist rest",
        "price": Decimal("229.99"),
        "currency": "USD",
        "category": "Gaming",
        "subcategory": "Gaming Keyboards",
        "brand": "Razer",
        "stock": 78,
        "rating": Decimal("4.6"),
        "review_count": 1234,
        "seller_id": "seller-009",
        "images": [
            {"url": "https://via.placeholder.com/400x400/00FF00/000000/?text=BlackWidow+V4", "alt_text": "BlackWidow V4 Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Fashion - Sneakers
    {
        "product_id": str(uuid.uuid4()),
        "title": "Nike Air Max 270",
        "description": "Men's Running Shoes, Max Air unit, Breathable mesh upper, Multiple colorways available",
        "price": Decimal("150.00"),
        "currency": "USD",
        "category": "Fashion",
        "subcategory": "Sneakers",
        "brand": "Nike",
        "stock": 234,
        "rating": Decimal("4.5"),
        "review_count": 5678,
        "seller_id": "seller-010",
        "images": [
            {"url": "https://via.placeholder.com/400x400/FF6B35/FFFFFF/?text=Air+Max+270", "alt_text": "Nike Air Max 270"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Adidas Ultraboost 22",
        "description": "Women's Running Shoes, Boost cushioning, Primeknit+ upper, Continental rubber outsole",
        "price": Decimal("190.00"),
        "currency": "USD",
        "category": "Fashion",
        "subcategory": "Sneakers",
        "brand": "Adidas",
        "stock": 167,
        "rating": Decimal("4.7"),
        "review_count": 4321,
        "seller_id": "seller-010",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Ultraboost+22", "alt_text": "Ultraboost 22"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Fashion - Watches
    {
        "product_id": str(uuid.uuid4()),
        "title": "Casio G-Shock GA-2100",
        "description": "Men's Analog-Digital Watch, Shock resistant, 200m water resistance, Carbon Core Guard structure",
        "price": Decimal("99.00"),
        "currency": "USD",
        "category": "Fashion",
        "subcategory": "Watches",
        "brand": "Casio",
        "stock": 345,
        "rating": Decimal("4.7"),
        "review_count": 8765,
        "seller_id": "seller-011",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FF0000/?text=G-Shock", "alt_text": "G-Shock GA-2100"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Fossil Gen 6 Hybrid Smartwatch",
        "description": "Analog watch face with smart features, Heart rate tracking, Notifications, 2-week battery life",
        "price": Decimal("229.00"),
        "currency": "USD",
        "category": "Fashion",
        "subcategory": "Watches",
        "brand": "Fossil",
        "stock": 89,
        "rating": Decimal("4.4"),
        "review_count": 1234,
        "seller_id": "seller-011",
        "images": [
            {"url": "https://via.placeholder.com/400x400/8B4513/FFFFFF/?text=Fossil+Gen+6", "alt_text": "Fossil Gen 6"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Office Supplies
    {
        "product_id": str(uuid.uuid4()),
        "title": "Herman Miller Aeron Office Chair",
        "description": "Ergonomic mesh office chair, Adjustable lumbar support, PostureFit SL, 12-year warranty",
        "price": Decimal("1395.00"),
        "currency": "USD",
        "category": "Office",
        "subcategory": "Furniture",
        "brand": "Herman Miller",
        "stock": 23,
        "rating": Decimal("4.8"),
        "review_count": 2345,
        "seller_id": "seller-012",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Aeron+Chair", "alt_text": "Aeron Chair"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Autonomous SmartDesk Pro",
        "description": "Electric standing desk, Dual motor, Memory presets, Anti-collision, 48x30 inch desktop",
        "price": Decimal("599.00"),
        "currency": "USD",
        "category": "Office",
        "subcategory": "Furniture",
        "brand": "Autonomous",
        "stock": 45,
        "rating": Decimal("4.6"),
        "review_count": 3456,
        "seller_id": "seller-012",
        "images": [
            {"url": "https://via.placeholder.com/400x400/FFFFFF/000000/?text=SmartDesk+Pro", "alt_text": "SmartDesk Pro"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    
    # Camera & Photography
    {
        "product_id": str(uuid.uuid4()),
        "title": "Canon EOS R6 Mark II Mirrorless Camera",
        "description": "24.2MP Full-Frame sensor, 40fps continuous shooting, 6K video, In-body image stabilization",
        "price": Decimal("2499.00"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Cameras",
        "brand": "Canon",
        "stock": 14,
        "rating": Decimal("4.9"),
        "review_count": 234,
        "seller_id": "seller-013",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Canon+R6+II", "alt_text": "Canon R6 Mark II"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "Sony Alpha a7 IV Mirrorless Camera",
        "description": "33MP Full-Frame sensor, Real-time Eye AF, 4K 60fps video, 10fps continuous shooting",
        "price": Decimal("2498.00"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Cameras",
        "brand": "Sony",
        "stock": 19,
        "rating": Decimal("4.8"),
        "review_count": 567,
        "seller_id": "seller-013",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Sony+a7+IV", "alt_text": "Sony a7 IV"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    {
        "product_id": str(uuid.uuid4()),
        "title": "DJI Mavic 3 Drone",
        "description": "Hasselblad camera, 5.1K video, 46-minute flight time, Omnidirectional obstacle sensing",
        "price": Decimal("2199.00"),
        "currency": "USD",
        "category": "Electronics",
        "subcategory": "Drones",
        "brand": "DJI",
        "stock": 31,
        "rating": Decimal("4.7"),
        "review_count": 892,
        "seller_id": "seller-013",
        "images": [
            {"url": "https://via.placeholder.com/400x400/000000/FFFFFF/?text=Mavic+3", "alt_text": "DJI Mavic 3"}
        ],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
]

def seed_products():
    print(f"Seeding {len(products)} products to DynamoDB...")
    
    for i, product in enumerate(products, 1):
        try:
            table.put_item(Item=product)
            print(f"✓ [{i}/{len(products)}] Added: {product['title']}")
        except Exception as e:
            print(f"✗ [{i}/{len(products)}] Failed to add {product['title']}: {str(e)}")
    
    print(f"\n🎉 Successfully seeded {len(products)} products!")
    print("\nProducts by Category:")
    categories = {}
    for product in products:
        cat = product['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count} products")

if __name__ == "__main__":
    seed_products()
