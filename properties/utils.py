from django.core.cache import cache
from .models import Property


def getall_properties():
    """
    Get all properties from cache or database.
    
    This function checks Redis cache for the 'all_properties' key first.
    If not found in cache, it fetches all properties from the database,
    stores them in cache for 1 hour (3600 seconds), and returns the queryset.
    
    Returns:
        QuerySet: All Property objects ordered by creation date (newest first)
    """

    cached_properties = cache.get('allproperties')
    
    if cached_properties is not None:

        return cached_properties
    
    queryset = Property.objects.all().order_by('-created_at')
    
    cache.set('allproperties', queryset, 3600)
    
    return queryset


def invalidate_properties_cache():
    """
    Utility function to invalidate the properties cache.
    This should be called when properties are created, updated, or deleted.
    """
    cache.delete('allproperties')