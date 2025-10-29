import json
import boto3
import os
import jwt
from decimal import Decimal
from datetime import datetime

def extract_user_from_token(event):
    """Extracts user ID from Authorization (JWT) header."""
    try:
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization") or headers.get("authorization")
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1]
        decoded = jwt.decode(token, options={"verify_signature": False})  # Don't verify in dev!
        return decoded.get("sub") or decoded.get("username")
    except Exception as e:
        print("Token extraction error", str(e))
        return None

def decimal_default(obj):
    """JSON serializer for Decimal objects."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def cors_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(body, default=decimal_default)
    }

dynamodb = boto3.resource("dynamodb", endpoint_url=os.getenv("AWSENDPOINTURL"))
CARTSTABLE = os.getenv("CARTSTABLE", "ekart-carts-dev")
PRODUCTSTABLE = os.getenv("PRODUCTSTABLE", "ekart-products-dev")

def get_cart(userid):
    """Returns the user's cart."""
    try:
        table = dynamodb.Table(CARTSTABLE)
        response = table.get_item(Key={"userid": userid})
        if "Item" not in response:
            return cors_response(200, {"userid": userid, "items": [], "totalamount": 0, "updatedat": datetime.utcnow().isoformat()})
        return cors_response(200, response["Item"])
    except Exception as e:
        print("Error getting cart", e)
        return cors_response(500, {"error": str(e)})

def add_to_cart(userid, body):
    """Adds an item to the user's cart."""
    try:
        productid = body['productid']
        quantity = int(body.get("quantity", 1))
        product_table = dynamodb.Table(PRODUCTSTABLE)
        prod_response = product_table.get_item(Key={"productid": productid})
        if "Item" not in prod_response:
            return cors_response(404, {"error": "Product not found"})
        product = prod_response["Item"]

        cart_table = dynamodb.Table(CARTSTABLE)
        cart_response = cart_table.get_item(Key={"userid": userid})
        items = cart_response.get("Item", {}).get("items", [])

        # See if product already in cart
        for item in items:
            if item["productid"] == productid:
                item["quantity"] += quantity
                break
        else:
            items.append({
                "productid": productid,
                "productname": product.get("title") or product.get("name", "Unknown Product"),
                "price": product["price"],
                "quantity": quantity,
                "sellerid": product.get("sellerid")
            })

        totalamount = sum(float(str(item["price"])) * item["quantity"] for item in items)
        cart = {
            "userid": userid,
            "items": items,
            "totalamount": totalamount,
            "updatedat": datetime.utcnow().isoformat()
        }
        cart_table.put_item(Item=cart)
        return cors_response(200, cart)
    except Exception as e:
        print("Error adding to cart", e)
        return cors_response(500, {"error": str(e)})

def update_cart_item(userid, productid, body):
    """Updates the quantity for a cart item."""
    try:
        quantity = int(body.get("quantity", 1))
        table = dynamodb.Table(CARTSTABLE)
        response = table.get_item(Key={"userid": userid})
        if "Item" not in response:
            return cors_response(404, {"error": "Cart not found"})
        cart = response["Item"]
        items = cart.get("items", [])

        found = False
        for item in items:
            if item["productid"] == productid:
                if quantity == 0:
                    items.remove(item)
                else:
                    item["quantity"] = quantity
                found = True
                break
        if not found:
            return cors_response(404, {"error": "Item not found in cart"})

        totalamount = sum(float(str(item["price"])) * item["quantity"] for item in items)
        cart["items"] = items
        cart["totalamount"] = totalamount
        cart["updatedat"] = datetime.utcnow().isoformat()
        table.put_item(Item=cart)
        return cors_response(200, cart)
    except Exception as e:
        print("Error updating cart", e)
        return cors_response(500, {"error": str(e)})

def remove_from_cart(userid, productid):
    """Removes a product from the cart."""
    try:
        table = dynamodb.Table(CARTSTABLE)
        response = table.get_item(Key={"userid": userid})
        if "Item" not in response:
            return cors_response(404, {"error": "Cart not found"})
        cart = response["Item"]
        items = [item for item in cart.get("items", []) if item["productid"] != productid]
        cart["items"] = items
        cart["totalamount"] = sum(float(str(item["price"])) * item["quantity"] for item in items)
        cart["updatedat"] = datetime.utcnow().isoformat()
        table.put_item(Item=cart)
        return cors_response(200, {"message": "Item removed from cart"})
    except Exception as e:
        print("Error removing from cart", e)
        return cors_response(500, {"error": str(e)})

def clear_cart(userid):
    """Clears the user's cart."""
    try:
        table = dynamodb.Table(CARTSTABLE)
        table.delete_item(Key={"userid": userid})
        return cors_response(200, {"message": "Cart cleared"})
    except Exception as e:
        print("Error clearing cart", e)
        return cors_response(500, {"error": str(e)})

def lambda_handler(event, context):
    print("Event", json.dumps(event))
    http_method = event.get("httpMethod", "")
    path = event.get("path", "")
    path_params = event.get("pathParameters") or {}
    productid = path_params.get("id") or path_params.get("productid")
    body = None
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except Exception:
            body = {}

    if http_method == "OPTIONS":
        return cors_response(200, {})

    userid = extract_user_from_token(event)
    if not userid:
        return cors_response(401, {"error": "Authentication required"})

    if http_method == "GET" and "items" not in path:
        return get_cart(userid)
    elif http_method == "POST" and "items" in path:
        return add_to_cart(userid, body)
    elif http_method == "PUT" and productid:
        return update_cart_item(userid, productid, body)
    elif http_method == "DELETE" and productid:
        return remove_from_cart(userid, productid)
    elif http_method == "DELETE":
        return clear_cart(userid)
    else:
        return cors_response(405, {"error": "Method not allowed"})
