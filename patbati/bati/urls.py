from patbati.bati.models import Bati
from mapentity.registry import registry

app_name = "bati"

urlpatterns = registry.register(Bati)