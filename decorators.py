"""
Logging decorators for the Address Book API.

This module provides decorators for logging function inputs and outputs
to help with debugging and monitoring API behavior.
"""

import logging

def log_input_output(logger_name: str = None):
   """
   Decorator to log function inputs and outputs.

   This decorator logs the function name, input arguments, and return values.
   It handles both regular functions and async functions.

   Args:
       logger_name (str, optional): Name of the logger to use.
                                  If None, uses the module name of the decorated function.

   Returns:
       Callable: Decorated function with input/output logging
   """
   def decorator(func):
       logger = logging.getLogger(logger_name)

       def wrapper(*args, **kwargs):
           func_name = func.__name__
           logger.info(f"Entering {func_name} with args: {args}, kwargs: {kwargs}")
           try:
               result = func(*args, **kwargs)
               logger.info(f"Exiting {func_name} with result: {result}")
               return result
           except Exception as e:
               logger.error(f"Exception in {func_name}: {e}")
               raise

       return wrapper

   return decorator
