from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Listing
from .choices import state_choices, price_choices, bedroom_choices

# Create your views here.


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    page_listings = paginator.get_page(page)

    context = {
        'listings': page_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):

    searchquery_list = Listing.objects.order_by('-list_date')

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            searchquery_list = searchquery_list.filter(
                description__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            searchquery_list = searchquery_list.filter(city__iexact=city)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            searchquery_list = searchquery_list.filter(state__iexact=state_choices[state])

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            searchquery_list = searchquery_list.filter(bedrooms__iexact=bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            searchquery_list = searchquery_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'price_choices': price_choices,
        'bedroom_choices': bedroom_choices,
        'listings': searchquery_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)
