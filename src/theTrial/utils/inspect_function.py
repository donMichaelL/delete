from inspect import Signature
from inspect import signature
from typing import Any
from typing import Callable
from typing import Tuple


def get_first_arg_type(sig: Signature, default: Any = None):
    """
    Get the type annotation of the first argument of a function signature.

    :param sig: The signature of the function.
    :param default: The default value to return if the function has no arguments.
    :return: The type annotation of the first argument or the default value.
    """
    try:
        annotation = list(sig.parameters.values())[0].annotation
        if annotation is Signature.empty:
            return default
        return annotation
    except IndexError:
        return default


def get_signature_details(func: Callable[..., Any]) -> Tuple[int, Any]:
    """
    Get the number of parameters and the type of the first argument of a function.

    :param func: The function to inspect.
    :return: A tuple containing the number of parameters and the
            type of the first argument.
    """
    sig = signature(func)

    return len(sig.parameters), get_first_arg_type(sig)
