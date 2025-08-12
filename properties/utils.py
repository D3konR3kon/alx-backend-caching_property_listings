
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
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
    
def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including:
              - keyspace_hits: Number of successful lookups of keys
              - keyspace_misses: Number of failed lookups of keys  
              - hit_ratio: Cache hit ratio as a percentage
              - total_requests: Total number of cache requests
    """
    try:

        redis_conn = get_redis_connection("default")

        info = redis_conn.info()

        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        total_requests = keyspace_hits + keyspace_misses
        
        # if total_requests > 0:
        #     hit_ratio = (keyspace_hits / total_requests) * 100
        # else:
        #     hit_ratio = 0.0
        
        if total_requests > 0 else 0

        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': round(hit_ratio, 2),
            'total_requests': total_requests
        }
        

        logger.info(f"Redis Cache Metrics - Hits: {keyspace_hits}, "
                   f"Misses: {keyspace_misses}, "
                   f"Hit Ratio: {hit_ratio:.2f}%, "
                   f"Total Requests: {total_requests}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'total_requests': 0,
            'error': str(e)
        }