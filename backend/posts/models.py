from django.contrib.postgres.search import SearchVector, SearchVectorField, TrigramSimilarity, SearchRank, SearchQuery
from django.contrib.postgres.aggregates import StringAgg
from django.db import models
from django.utils import timezone


# Create your models here.
class PostManager(models.Manager):
    def search(self, search_text):
        search_vectors = (
            SearchVector(
                'title',
                weight='A',
                config='english'
            )
            + SearchVector(
                StringAgg('message', delimiter=' '),
                weight='B',
                config='english',
            )
        )
        search_query = SearchQuery(
            search_text, config='english'
        )
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity(
            'title', search_text
        )
        queryset = (
            self.get_queryset()
            .filter(search_vector=search_query)
            .annotate(rank=search_rank + trigram_similarity)
            .order_by('-rank')
        )
        return queryset


class Post(models.Model):
    class Meta:
        db_table = 'Post'

    title = models.CharField(max_length=255, blank=False, null=False)
    message = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)

    search_vector = SearchVectorField(null=True)
    objects = PostManager()

    def __str__(self):
        return '{}: {}'.format(self.author.username, self.title)

    def save(self, *args, **kwargs):
        self.search_vector = (
                SearchVector('title', weight='A')
                + SearchVector('message', weight='B')
        )
        super().save(*args, **kwargs)
