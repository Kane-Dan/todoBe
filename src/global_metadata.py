from .tasks.models import metadata as tasks_meta
from .users.models import metadata as users_meta
from .auth.models import metadata as auth_meta

metadata = [tasks_meta, users_meta, auth_meta]