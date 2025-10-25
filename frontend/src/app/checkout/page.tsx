'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { Button } from '@/components/ui/Button';
import { ArrowLeft } from 'lucide-react';

interface CartItem {
  product_id: string;
  quantity: number;
  added_at: string;
}

interface Cart {
  user_id: string;
  items: CartItem[];
}

interface Product {
  product_id: string;
  title: string;
  price: number;
  image_url?: string;
}

// CheckoutForm component
function CheckoutForm({ clientSecret, amount }: { clientSecret: string; amount: number }) {
  const stripe = useStripe();
  const elements = useElements();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [succeeded, setSucceeded] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);
    setError(null);

    try {
      const { error: submitError } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/checkout/success`,
        },
      });

      if (submitError) {
        setError(submitError.message || 'Payment failed');
        setProcessing(false);
      } else {
        setSucceeded(true);
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Payment Details</h2>
        
        <div className="mb-6">
          <div className="flex justify-between text-lg font-semibold mb-4">
            <span>Total Amount:</span>
            <span className="text-blue-600">${amount.toFixed(2)}</span>
          </div>
        </div>

        <PaymentElement />

        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded text-red-600 text-sm">
            {error}
          </div>
        )}

        <div className="mt-6 flex gap-4">
          <Button
            type="button"
            variant="outline"
            onClick={() => router.back()}
            disabled={processing || succeeded}
            className="flex-1"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Cart
          </Button>
          
          <Button
            type="submit"
            disabled={!stripe || processing || succeeded}
            className="flex-1"
          >
            {processing ? 'Processing...' : succeeded ? 'Payment Successful!' : 'Pay Now'}
          </Button>
        </div>
      </div>
    </form>
  );
}

export default function CheckoutPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [products, setProducts] = useState<Map<string, Product>>(new Map());
  const [loading, setLoading] = useState(true);
  const [clientSecret, setClientSecret] = useState<string | null>(null);
  const [stripePromise, setStripePromise] = useState<any>(null);
  const [totalAmount, setTotalAmount] = useState(0);
  const router = useRouter();

  useEffect(() => {
    initializeCheckout();
  }, []);

  const initializeCheckout = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        router.push('/auth/login');
        return;
      }

      // Get Stripe config
      const configResponse = await fetch('http://localhost:8000/api/payments/config');
      const config = await configResponse.json();
      
      // Initialize Stripe with LocalStack endpoint
      const stripeInstance = await loadStripe(config.publishable_key, {
        apiVersion: '2023-10-16',
        // Point to LocalStack Stripe extension
        stripeAccount: undefined,
      });
      setStripePromise(stripeInstance);

      // Fetch cart
      const cartResponse = await fetch('http://localhost:8000/api/cart/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!cartResponse.ok) {
        throw new Error('Failed to fetch cart');
      }

      const cartData = await cartResponse.json();
      setCart(cartData);

      if (!cartData.items || cartData.items.length === 0) {
        router.push('/cart');
        return;
      }

      // Fetch product details for all items
      const productPromises = cartData.items.map((item: CartItem) =>
        fetch(`http://localhost:8000/api/products/${item.product_id}`)
          .then(res => res.json())
      );

      const productsData = await Promise.all(productPromises);
      const productsMap = new Map();
      let total = 0;

      productsData.forEach((product: Product, index: number) => {
        productsMap.set(product.product_id, product);
        const quantity = cartData.items[index].quantity;
        total += product.price * quantity;
      });

      setProducts(productsMap);
      setTotalAmount(total);

      // Create payment intent
      const paymentResponse = await fetch('http://localhost:8000/api/payments/create-payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          currency: 'usd',
          metadata: {
            cart_items: JSON.stringify(cartData.items.map((item: CartItem) => ({
              product_id: item.product_id,
              quantity: item.quantity
            })))
          }
        })
      });

      if (!paymentResponse.ok) {
        throw new Error('Failed to create payment intent');
      }

      const paymentData = await paymentResponse.json();
      setClientSecret(paymentData.client_secret);

    } catch (error) {
      console.error('Error initializing checkout:', error);
      alert('Failed to initialize checkout. Please try again.');
      router.push('/cart');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading checkout...</p>
        </div>
      </div>
    );
  }

  if (!clientSecret || !stripePromise) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-red-600 mb-4">Failed to initialize payment system</p>
          <Button onClick={() => router.push('/cart')}>
            Return to Cart
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8">Checkout</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-8">
              <h2 className="text-xl font-bold mb-4">Order Summary</h2>
              
              <div className="space-y-3 mb-4">
                {cart?.items.map((item) => {
                  const product = products.get(item.product_id);
                  if (!product) return null;

                  return (
                    <div key={item.product_id} className="flex justify-between text-sm">
                      <div className="flex-1">
                        <p className="font-medium truncate">{product.title}</p>
                        <p className="text-gray-500">Qty: {item.quantity}</p>
                      </div>
                      <p className="font-semibold ml-4">
                        ${(product.price * item.quantity).toFixed(2)}
                      </p>
                    </div>
                  );
                })}
              </div>

              <div className="border-t pt-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Subtotal:</span>
                  <span>${totalAmount.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Shipping:</span>
                  <span>Free</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t pt-2">
                  <span>Total:</span>
                  <span className="text-blue-600">${totalAmount.toFixed(2)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Payment Form */}
          <div className="lg:col-span-2">
            <Elements stripe={stripePromise} options={{ clientSecret }}>
              <CheckoutForm clientSecret={clientSecret} amount={totalAmount} />
            </Elements>
          </div>
        </div>
      </div>
    </div>
  );
}
