from import_export import resources
from .models import Students

class PersonResource(resources.ModelResource):
    class meta:
        model = Students