import griddle
import noiftimer
import printbuddies

from .pathier import Pathier, Pathish, Pathy

__all__ = ["Pathier", "Pathy", "Pathish"]


@noiftimer.time_it()
def sizeup():
    """Print the sub-directories and their sizes of the current working directory."""
    sizes: dict[str, int] = {}
    folders = [folder for folder in Pathier.cwd().iterdir() if folder.is_dir()]
    print(f"Sizing up {len(folders)} directories...")
    with printbuddies.ProgBar(len(folders)) as prog:
        for folder in folders:
            prog.display(f"Scanning '{folder.name}'")
            sizes[folder.name] = folder.size
    total_size = sum(sizes[folder] for folder in sizes)
    size_list = [
        (folder, Pathier.format_bytes(sizes[folder]))
        for folder in sorted(list(sizes.keys()), key=lambda f: sizes[f], reverse=True)
    ]
    print(griddle.griddy(size_list, ["Dir", "Size"]))
    print(f"Total size of '{Pathier.cwd()}': {Pathier.format_bytes(total_size)}")


__version__ = "1.5.1"
