"""Python wrapper for Tailwind CSS v3.1.5."""
import logging
import sys
import typing
from pathlib import Path
from subprocess import call, run

__all__ = [
    "init",
    "build",
    "watch",
]
__title__ = "tailwind"
__description__ = "Python wrapper for Tailwind CSS v3.1.5."
__author__ = "Seyeong Jeong"
__author_email__ = "seyeng@jeo.ng"
__license__ = "MIT"
__copyright__ = "Copyright 2022 Seyeong Jeong"
__version__ = "3.1.5b0"

_RELATIVE_TAIWIND_BIN = "bin/tailwindcss-macos-arm64"
TAILWIND_BIN = str(Path(__file__).parent.resolve().joinpath(_RELATIVE_TAIWIND_BIN))
TAILWIND_VERSION = "v3.1.5"

logger = logging.getLogger(__name__)


class TailwindError(RuntimeError):
    """Top level Tailwind error."""


class InitError(TailwindError):
    """Initialization error."""


class ConfigFileExistsError(InitError):
    """Configuration file already exists error."""


class BuildError(TailwindError):
    """Build error."""


def _log_stderr(message: str) -> None:
    logger.warning(message)


def init(full: bool = False, postcss: bool = False) -> None:
    """Initialize Tailwind CSS environment."""
    options = ["init"]
    if full:
        options.append("--full")

    if postcss:
        options.append("--postcss")

    try:
        logger.debug("Invoking tailwind with %s options.", options)
        response = run(
            [TAILWIND_BIN] + options,
            capture_output=True,
            check=True,
        )
    except Exception as exc:
        raise InitError(f"Initi error occured with {options} options.") from exc

    if response.stderr:
        _log_stderr(response.stderr.decode())

    stdout = response.stdout.decode()
    if "already exists" in stdout:
        raise ConfigFileExistsError(stdout)


def _build_options(
    input: typing.Union[str, Path, None] = None,
    output: typing.Union[str, Path, None] = None,
    content: typing.Union[str, None] = None,
    postcss: typing.Union[bool, Path, str] = False,
    minify: bool = False,
    config: typing.Union[str, Path, None] = None,
    autoprefixer: bool = True,
) -> typing.List[str]:
    options = ["build"]

    if input is not None:
        options.append("--input")
        options.append(str(input))

    if output is not None:
        options.append("--output")
        options.append(str(output))

    if content is not None:
        options.append("--content")
        options.append(content)

    if postcss:
        options.append("--postcss")
        if isinstance(postcss, (Path, str)):
            options.append(str(postcss))

    if minify:
        options.append("--minify")

    if config is not None:
        options.append("--config")
        options.append(str(config))

    if not autoprefixer:
        options.append("--no-autoprefixer")

    return options


def build(
    input: typing.Union[str, Path, None] = None,
    output: typing.Union[str, Path, None] = None,
    content: typing.Union[str, None] = None,
    postcss: typing.Union[bool, Path, str] = False,
    minify: bool = False,
    config: typing.Union[str, Path, None] = None,
    autoprefixer: bool = True,
) -> typing.Union[str, None]:
    """Build Tailwind CSS."""
    options = _build_options(
        input=input,
        output=output,
        content=content,
        postcss=postcss,
        minify=minify,
        config=config,
        autoprefixer=autoprefixer,
    )
    try:
        logger.debug("Invoking tailwind with %s options.", options)
        response = run(
            [TAILWIND_BIN] + options,
            capture_output=True,
            check=True,
        )
    except Exception as exc:
        raise BuildError(f"Build error occured with {options}.") from exc

    if response.stderr:
        _log_stderr(response.stderr.decode())

    if output is None:
        return response.stdout.decode()

    return None


def watch(
    input: typing.Union[str, Path, None] = None,
    output: typing.Union[str, Path, None] = None,
    content: typing.Union[str, None] = None,
    postcss: typing.Union[bool, Path, str] = False,
    minify: bool = False,
    config: typing.Union[str, Path, None] = None,
    autoprefixer: bool = True,
    poll: bool = False,
) -> None:
    """Watch Tailwind CSS."""
    options = _build_options(
        input=input,
        output=output,
        content=content,
        postcss=postcss,
        minify=minify,
        config=config,
        autoprefixer=autoprefixer,
    )
    if poll:
        options.append("--poll")
    else:
        options.append("--watch")

    try:
        logger.debug("Invoking tailwind with %s options.", options)
        run(
            [TAILWIND_BIN] + options,
            check=True,
        )
    except Exception as exc:
        raise BuildError(f"Build error occured with {options}.") from exc


def main() -> int:
    """Invoke Tailwind CSS directly with arugments."""
    argv = sys.argv[1:]
    logger.debug("Invoking tailwind with %s options.", argv)
    return call([TAILWIND_BIN] + argv)


if __name__ == "__main__":
    sys.exit(main())
