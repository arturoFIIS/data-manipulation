from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q, Subquery, OuterRef
from django.utils import timezone
from datetime import timedelta
from .models import Customer, Interaction

def customer_list(request):
    # Obtener última interacción por cliente (optimizado)
    last_interaction = Interaction.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-date').values('type', 'date')[:1]
    
    customers = Customer.objects.select_related('company', 'agent').annotate(
        last_interaction_type=Subquery(last_interaction.values('type')),
        last_interaction_date=Subquery(last_interaction.values('date'))
    )
    
    # Filtros
    search = request.GET.get('search', '')
    if search:
        customers = customers.filter(Q(name__icontains=search))
    
    # Filtro por cumpleaños
    birthday_filter = request.GET.get('birthday_filter', '')
    if birthday_filter == 'this_week':
        today = timezone.now().date()
        week_end = today + timedelta(days=7)
        customers = customers.filter(
            birth_date__month=today.month,
            birth_date__day__gte=today.day,
            birth_date__day__lte=week_end.day
        )
    elif birthday_filter == 'this_month':
        today = timezone.now().date()
        customers = customers.filter(birth_date__month=today.month)
    
    # Ordenamiento
    order_by = request.GET.get('order_by', 'name')
    order_map = {
        'name': 'name',
        'company': 'company__name',
        'birthday': 'birth_date',
        'last_interaction': '-last_interaction_date'
    }
    customers = customers.order_by(order_map.get(order_by, 'name'))
    
    # Paginación
    paginator = Paginator(customers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'core/customer_list.html', {
        'page_obj': page_obj,
        'search': search,
        'order_by': order_by,
        'birthday_filter': birthday_filter
    })