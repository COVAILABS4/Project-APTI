from django.shortcuts import render

# Create your views here.
def index(request):
    """Render the main template."""
    return render(request, 'server/index.html')