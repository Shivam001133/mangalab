

def get_chaper_no(chapter_name=None):
    if chapter_name:
        chapter_name = chapter_name.strip().split(' ')
        chapter_no = [i for i in chapter_name if i.isdigit()]
        return chapter_no[0]
    return None


def get_paginated_data_from_list(request, query_data):
    from django.core.paginator import Paginator, EmptyPage
    items_per_page = 12
    paginator = Paginator(query_data, items_per_page)
    current_page = int(request.GET.get('page', int(1)))
    try:
        current_page_data = paginator.page(current_page)
    except EmptyPage:
        current_page_data = paginator.page(1)
    next_page = None
    prev_page = None
    if current_page_data.has_next():
        next_page = request.build_absolute_uri(
            f'?page={current_page_data.next_page_number()}')
    if current_page_data.has_previous():
        prev_page = request.build_absolute_uri(
            f'?page={current_page_data.previous_page_number()}')
    paginated_data = {
        "count": paginator.count,
        'previous': prev_page,
        'next': next_page,
        "results": current_page_data.object_list,
    }
    return paginated_data


def get_paginated_data(request, query_data):
    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_manga_list = paginator.paginate_queryset(query_data, request)
    # paginated_manga_list['new'] = 'new data'
    return paginator, paginated_manga_list
