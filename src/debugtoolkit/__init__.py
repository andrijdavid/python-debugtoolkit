from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

from .decorators import (  # noqa F401
    log_garbage_collection,
    log_inputs,
    log_time_execution,
    monitor_detailed_resources,
    monitor_resources,
)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "debugtoolkit"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
