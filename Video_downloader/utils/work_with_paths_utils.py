from pathlib import Path


def directory_check_and_creation(path_to_dir) -> str:
    path_to_save = Path(path_to_dir)
    if not Path(path_to_save).exists():
        Path.mkdir(Path(path_to_save), parents=True)
    return str(path_to_save)

# https://www.youtube.com/watch?v=bpkKaubIAv4
# https://www.youtube.com/watch?v=Fok17zwfXAY&list=PLAk6CfuV7hypidDmjEYvKK5JRlnmanmzR