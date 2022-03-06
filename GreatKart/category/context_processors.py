from .models import Category


def menu_links(request):
    """Function producing categories in dropdown menu of navbar as a dictionary"""
    links = Category.objects.all()
    return dict(links=links)
