from typing import Optional

from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...decorators import query_debugger
from .mixin import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    @query_debugger
    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            self.get_queryset(), self.paginate_by
        )

        prev_page: Optional[int] = (
            page.previous_page_number() if page.has_previous() else None
        )
        next_page: Optional[int] = (
            page.next_page_number() if page.has_next() else None
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(page.object_list),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    @query_debugger
    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        return super().get_context_data(**kwargs).get('object')
