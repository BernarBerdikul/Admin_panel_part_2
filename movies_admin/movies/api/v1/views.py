from django.http import Http404
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from .mixin import MoviesApiMixin
from ...decorators import query_debugger
from ...models import FilmWork
from typing import Optional, List


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    @query_debugger
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        context: List[dict] = [
            {
                "id": film_work.id,
                "title": film_work.title,
                "description": film_work.description,
                "creation_date": film_work.creation_date,
                "rating": film_work.rating,
                "type": film_work.type,
                "genres": film_work.genres_arr,
                "actors": film_work.actors_arr,
                "directors": film_work.directors_arr,
                "writers": film_work.writers_arr,
            }
            for film_work in queryset
        ]

        _prev: Optional[int] = (
            page.previous_page_number() if page.has_previous() else None
        )
        _next: Optional[int] = (
            page.next_page_number() if page.has_next() else None
        )
        return {
            'count': paginator.count,
            "total_pages": paginator.num_pages,
            "prev": _prev,
            "next": _next,
            "results": context
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_object(self, queryset=None):
        try:
            return self.get_queryset().get(
                id=self.kwargs.get(self.pk_url_kwarg, None)
            )
        except FilmWork.DoesNotExist:
            raise Http404('Ох, объекта нет')

    @query_debugger
    def get_context_data(self, *, object_list=None, **kwargs):
        film_work = self.get_object(queryset=self.get_queryset())
        context = {
            "id": film_work.id,
            "title": film_work.title,
            "description": film_work.description,
            "creation_date": film_work.creation_date,
            "rating": film_work.rating,
            "type": film_work.type,
            "genres": film_work.genres_arr,
            "actors": film_work.actors_arr,
            "directors": film_work.directors_arr,
            "writers": film_work.writers_arr,
        }
        return context
