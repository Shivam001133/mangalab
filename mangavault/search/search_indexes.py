from haystack import indexes
from mangavault.models import MangaVault


class MangaVaultIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr="title")
    manga_title = indexes.CharField(model_attr="manga_title")
    description = indexes.CharField(model_attr="description")

    def get_model(self):
        return MangaVault

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
