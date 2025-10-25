'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Trash2, Plus, Minus } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface CartItem {
  product_id: string;
  quantity: number;
  added_at: string;
}

interface Cart {
  user_id: string;
  items: CartItem[];
}

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/cart`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setCart(data);
      }
    } catch (error) {
      console.error('Error fetching cart:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeItem = async (productId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/cart/items/${productId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        fetchCart();
      }
    } catch (error) {
      console.error('Error removing item:', error);
    }
  };

  const updateQuantity = async (productId: string, newQuantity: number) => {
    if (newQuantity < 1) return;

    try {
      const token = localStorage.getItem('access_token');
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/cart/items/${productId}?quantity=${newQuantity}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        fetchCart();
      }
    } catch (error) {
      console.error('Error updating quantity:', error);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading cart...</div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600 mb-4">Your cart is empty</p>
          <Button onClick={() => router.push('/products')}>
            Continue Shopping
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Shopping Cart</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            {cart.items.map((item) => (
              <div key={item.product_id} className="p-6 border-b border-gray-200 last:border-b-0">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Product ID: {item.product_id.substring(0, 8)}...
                    </h3>
                    <p className="text-sm text-gray-500">Added: {new Date(item.added_at).toLocaleDateString()}</p>
                  </div>

                  <div className="flex items-center space-x-4">
                    {/* Quantity Controls */}
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                        className="p-1 rounded border border-gray-300 hover:bg-gray-100"
                        aria-label="Decrease quantity"
                      >
                        <Minus className="w-4 h-4" />
                      </button>
                      <span className="w-8 text-center">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                        className="p-1 rounded border border-gray-300 hover:bg-gray-100"
                        aria-label="Increase quantity"
                      >
                        <Plus className="w-4 h-4" />
                      </button>
                    </div>
                    {/* Remove Button */}
                    <button
                      onClick={() => removeItem(item.product_id)}
                      className="text-red-600 hover:text-red-800"
                      aria-label="Remove item from cart"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Order Summary</h2>
            
            <div className="space-y-2 mb-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Items:</span>
                <span className="font-semibold">{cart.items.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Quantity:</span>
                <span className="font-semibold">
                  {cart.items.reduce((sum, item) => sum + item.quantity, 0)}
                </span>
              </div>
            </div>

            <Button 
              className="w-full" 
              size="lg"
              onClick={() => router.push('/checkout')}
            >
              Proceed to Checkout
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
