from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse

from ...models import FilmWork, PersonType


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]  # Список методов, которые реализует обработчик

    @staticmethod
    def _aggregate_person(role):
        return ArrayAgg(
            "persons__full_name", distinct=True,
            filter=Q(personfilmwork__role=role)
        )

    def get_queryset(self):
        return self.model.objects.prefetch_related(
            "genres", "persons"
        ).values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type"
        ).annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=self._aggregate_person(role=PersonType.ACTOR),
            writers=self._aggregate_person(role=PersonType.WRITER),
            directors=self._aggregate_person(role=PersonType.DIRECTOR),
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
