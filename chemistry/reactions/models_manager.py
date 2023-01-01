from django.db import models


class ReactCompoundQuerySet(models.QuerySet):
    def for_reaction(self, reaction):
        return self.filter(reaction=reaction)