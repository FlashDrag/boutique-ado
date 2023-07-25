from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .models import Product


def all_products(request):
    """A view to show all products, including sorting and
    search queries"""
    products = Product.objects.all()
    query = None

    if request.GET:
        if "q" in request.GET:
            query = request.GET.get("q")
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse("products"))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query
            )
            products = products.filter(queries)

    context = {
        "products": products,
        "search_term": query,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """A view to show individual product detail"""

    product = get_object_or_404(Product, pk=product_id)
    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
