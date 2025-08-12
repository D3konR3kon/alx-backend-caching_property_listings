from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
def invalidate_properties_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    cache.delete('allproperties')
    
    # Optional: Log the cache invalidation for debugging
    action = "created" if created else "updated"
    print(f"Property '{instance.title}' was {action}. Cache invalidated.")


@receiver(post_delete, sender=Property)
def invalidate_properties_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    
    Args:
        sender: The model class (Property)
        instance: The actual instance being deleted
        **kwargs: Additional keyword arguments
    """
    cache.delete('allproperties')
    
    print(f"Property '{instance.title}' was deleted. Cache invalidated.")

