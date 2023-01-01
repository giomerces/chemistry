from django.db import models


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseNameMixin(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        abstract = True
        
class ChemistryModelMixin(BaseTimestampedModel):

    class Meta:
        abstract = True

