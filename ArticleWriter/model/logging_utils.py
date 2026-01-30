from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from colorama import Fore, Style, init


_INITIALIZED = False


def init_logging() -> None:
    """
    Initialize colorama once (safe to call multiple times).
    """
    global _INITIALIZED
    if _INITIALIZED:
        return
    init(autoreset=True)
    _INITIALIZED = True


@dataclass(frozen=True)
class LogColors:
    info: str = Fore.CYAN
    success: str = Fore.GREEN
    warning: str = Fore.YELLOW
    error: str = Fore.RED
    dim: str = Style.DIM
    reset: str = Style.RESET_ALL

    # "Pink" for prompts (closest terminal color): light magenta
    prompt: str = Fore.LIGHTMAGENTA_EX


_C = LogColors()


def info(msg: str) -> None:
    init_logging()
    print(f"{_C.info}{msg}{_C.reset}")


def success(msg: str) -> None:
    init_logging()
    print(f"{_C.success}{msg}{_C.reset}")


def warning(msg: str) -> None:
    init_logging()
    print(f"{_C.warning}{msg}{_C.reset}")


def error(msg: str) -> None:
    init_logging()
    print(f"{_C.error}{msg}{_C.reset}")


def dim(msg: str) -> None:
    init_logging()
    print(f"{_C.dim}{msg}{_C.reset}")


def prompt_pink(msg: str) -> None:
    """
    Print the Nano Banana prompt in pink/magenta.
    """
    init_logging()
    print(f"{_C.prompt}{msg}{_C.reset}")

