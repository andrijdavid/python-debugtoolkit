import gc
import logging
import os
import time
from functools import wraps

import psutil

# Setting up a basic logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def safe_repr(obj):
    """
    Generate a safe representation of the object for logging.
    Avoids calling the __repr__ method of the object directly.
    """
    if isinstance(obj, (int, float, str, bool)):
        return repr(obj)  # Safe to use repr for basic types
    return f"<{type(obj).__name__} object at {hex(id(obj))}>"


def log_inputs(func):
    """
    This is a decorator function that logs the input arguments of the decorated function.

    It logs the function call with its arguments and keyword arguments, using a safe_repr function to convert the arguments to a string representation. The log message is in the format of "Calling {function_name}({arguments})".

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function which logs its input arguments when called.

    Example:
        @log_inputs
        def add(a, b):
            return a + b

        add(1, 2)
        # The above call will log "Calling add(1, 2)"
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [safe_repr(a) for a in args]  # Use safe_repr for arguments
        kwargs_repr = [
            f"{k}={safe_repr(v)}" for k, v in kwargs.items()
        ]  # Use safe_repr for keyword arguments
        signature = ", ".join(args_repr + kwargs_repr)
        logging.info(f"Calling {func.__name__}({signature})")
        return func(*args, **kwargs)

    return wrapper


def log_time_execution(n=1):
    """
    This is a decorator function that logs the execution time of the decorated function.

    It runs the function n times, and logs the execution time for each run. If n is greater than 1, it also logs the average execution time.

    Args:
        n (int, optional): The number of times to run the decorated function. Defaults to 1.

    Returns:
        function: The decorated function which logs its execution time when called.

    Example:
        @log_time_execution(n=3)
        def add(a, b):
            return a + b

        add(1, 2)
        # The above call will log the execution time for each of the 3 runs,
        # and the average execution time.

    """

    def decorator_time(func):
        @wraps(func)
        def wrapper_time(*args, **kwargs):
            times = []
            result = None
            for i in range(n):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                times.append(end_time - start_time)
                logging.info(
                    f"Execution {i + 1} of {func.__name__}: {times[-1]:.6f} seconds"
                )
            if n > 1:
                logging.info(
                    f"Average execution time of {func.__name__}: {sum(times) / n:.6f} seconds"
                )
            return result

        return wrapper_time

    return decorator_time


def log_garbage_collection(func):
    """
    This is a decorator function that logs the garbage collection counts before and after the execution of the decorated function.

    It checks the garbage collection counts before and after the function execution. If the counts have changed, it logs the counts before and after the execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function which logs its garbage collection counts when called.

    Example:
        @log_garbage_collection
        def add(a, b):
            return a + b

        add(1, 2)
        # The above call will log the garbage collection counts before and after the function execution if they have changed.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        gc_counts_before = gc.get_count()
        result = func(*args, **kwargs)
        gc_counts_after = gc.get_count()

        if gc_counts_before != gc_counts_after:
            logging.info(
                f"Garbage collection counts changed for {func.__name__}: "
                f"Before: {gc_counts_before}, After: {gc_counts_after}"
            )

        return result

    return wrapper


def monitor_detailed_resources(func):
    """
    This is a decorator function that logs the detailed resource usage of the decorated function.

    It calculates and logs the CPU usage, execution time, memory usage, disk I/O, and network I/O before and after the function execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function which logs its detailed resource usage when called.

    Example:
        @monitor_detailed_resources
        def add(a, b):
            return a + b

        add(1, 2)
        # The above call will log the detailed resource usage of the function execution.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        cpu_before = process.cpu_percent(interval=None)
        mem_before = process.memory_info()
        disk_io_before = psutil.disk_io_counters()
        net_io_before = psutil.net_io_counters()
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        cpu_after = process.cpu_percent(interval=None)
        mem_after = process.memory_info()
        disk_io_after = psutil.disk_io_counters()
        net_io_after = psutil.net_io_counters()

        # Logging detailed resource usage
        logging.info(f"Resource usage for {func.__name__}:")
        logging.info(f"CPU Usage: {cpu_after - cpu_before}%")
        logging.info(f"Execution Time: {end_time - start_time} seconds")
        logging.info(
            f"Memory Usage: RSS: {mem_after.rss - mem_before.rss} bytes, "
            f"VMS: {mem_after.vms - mem_before.vms} bytes"
        )
        logging.info(
            f"Disk I/O: Read: {disk_io_after.read_bytes - disk_io_before.read_bytes} bytes, "
            f"Write: {disk_io_after.write_bytes - disk_io_before.write_bytes} bytes"
        )
        logging.info(
            f"Network I/O: Sent: {net_io_after.bytes_sent - net_io_before.bytes_sent} bytes, "
            f"Received: {net_io_after.bytes_recv - net_io_before.bytes_recv} bytes"
        )

        return result

    return wrapper


def monitor_resources(func):
    """
    This is a decorator function that logs the CPU and memory usage of the decorated function.

    It calculates the CPU usage and memory usage before and after the function execution, and logs the difference. The CPU usage is logged as a percentage, and the memory usage is logged in bytes.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function which logs its CPU and memory usage when called.

    Example:
        @monitor_resources
        def add(a, b):
            return a + b

        add(1, 2)
        # The above call will log the CPU and memory usage of the function execution.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get initial resource usage
        process = psutil.Process(os.getpid())
        cpu_before = process.cpu_percent(interval=None)
        memory_before = process.memory_info()

        result = func(*args, **kwargs)

        # Get resource usage after function execution
        cpu_after = process.cpu_percent(interval=None)
        memory_after = process.memory_info()

        # Log the resource usage
        logging.info(
            f"Resource usage for {func.__name__}: "
            f"CPU: {cpu_after - cpu_before}%, "
            f"Memory: {memory_after.vms - memory_before.vms} bytes"
        )

        return result

    return wrapper
