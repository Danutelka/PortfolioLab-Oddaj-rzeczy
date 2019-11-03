from django.http import HttpResponse
from oddaj.models import Institution, Category

def get_institution(request):
    cat_ids = request.GET.get('ids','')
    cat_ids = cat_ids.split(",")
    cats = Category.objects.filter(id__in=cat_ids)
    inst = Institution.objects.filter(categories__in=cats)
    return HttpResponse(create_select_from_queryset(inst))


def create_select_from_queryset(queryset):
    s=""
    for item in queryset:
        s+= f"<option  value={item.id}>{item.name}</option>"
    return s


