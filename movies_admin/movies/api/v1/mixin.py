from django.http import JsonResponse
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from ...models import FilmWork, PersonType


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get_queryset(self):
        return self.model.objects.prefetch_related(
            "genres", "persons"
        ).annotate(
            genres_arr=ArrayAgg("genres__name", distinct=True),
            actors_arr=ArrayAgg(
                "persons__full_name", distinct=True,
                filter=Q(personfilmwork__role=PersonType.ACTOR)
            ),
            writers_arr=ArrayAgg(
                "persons__full_name", distinct=True,
                filter=Q(personfilmwork__role=PersonType.WRITER)
            ),
            directors_arr=ArrayAgg(
                "persons__full_name", distinct=True,
                filter=Q(personfilmwork__role=PersonType.DIRECTOR)
            ),
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
