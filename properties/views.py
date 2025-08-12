from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from .utils import get_all_properties
import json


@cache_page(60 * 15)  
def property_list(request):
    """
    View to display all properties with caching, pagination, and search functionality
    """
   
    search_query = request.GET.get('search', '')
    
    properties = get_all_properties()
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    

    paginator = Paginator(properties, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    if request.GET.get('format') == 'json':
        return property_list_json(request, page_obj, search_query)
    
   
    context = {
        'properties': page_obj,
        'search_query': search_query,
        'total_properties': properties.count(),
    }
    
    return render(request, 'properties/property_list.html', context)


def property_list_json(request, page_obj, search_query):
    """
    Return JSON response for property list
    """
    properties_data = []
    
    for property in page_obj:
        properties_data.append({
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),
            'formatted_price': property.formatted_price(),
            'location': property.location,
            'created_at': property.created_at.isoformat(),
        })
    
    response_data = {
        'properties': properties_data,
        'pagination': {
            'current_page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
            'total_count': page_obj.paginator.count,
        },
        'search_query': search_query,
    }
    
    return JsonResponse(response_data)


@cache_page(60 * 15) 
def property_detail(request, property_id):
    """
    View to display a single property with caching
    """
    try:
        property = Property.objects.get(id=property_id)

        if request.GET.get('format') == 'json':
            property_data = {
                'id': property.id,
                'title': property.title,
                'description': property.description,
                'price': str(property.price),
                'formatted_price': property.formatted_price(),
                'location': property.location,
                'created_at': property.created_at.isoformat(),
            }
            return JsonResponse({'property': property_data})
        

        context = {'property': property}
        return render(request, 'properties/property_detail.html', context)
        
    except Property.DoesNotExist:
        if request.GET.get('format') == 'json':
            return JsonResponse({'error': 'Property not found'}, status=404)
        return render(request, 'properties/property_not_found.html', status=404)


def clear_cache(request):
    """
    Utility view to clear cache (useful for development and testing)
    """
    from django.core.cache import cache
    from .utils import invalidate_properties_cache
    

    cache.clear()
    
    invalidate_properties_cache()
    
    if request.GET.get('format') == 'json':
        return JsonResponse({'message': 'Cache cleared successfully'})
    
    return render(request, 'properties/cache_cleared.html')