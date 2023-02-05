from django.shortcuts import render

# Create your views here.
from django.views import View
import stripe
from  django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Product
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)
    
class ProductLandingPageView(TemplateView): 
    template_name = 'landing.html'
    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Example Item")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product": product, 
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context
    
    
class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
