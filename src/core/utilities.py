from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(page_number, items, per_page=10):
    orphans = min(per_page, 2)
    paginator = Paginator(items, per_page, orphans=orphans)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        if page_number <= 0:
            page = paginator.page(1)
        else:
            page = paginator.page(paginator.num_pages)
    return page, paginator.get_elided_page_range(page.number, on_each_side=1)
