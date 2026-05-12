from pathlib import Path, PurePath
from PIL import Image
import pillow_heif
from shutil import rmtree


cwd = Path.cwd()
input_dir = cwd / "input"
output_dir = cwd / "output"

def main():
    Path(output_dir).mkdir(exist_ok=True)

    for path in output_dir.iterdir():
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()

    for entry in input_dir.iterdir():
        if entry.is_file() and entry.name.upper().endswith(".HEIC"):
            print(f"🔄 Converting {entry.name}...")
            heif_file = pillow_heif.read_heif(entry.absolute())
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
            file_name = f"{entry.stem}.png"
            file_path = PurePath(output_dir, file_name)
            image.save(file_path, format("png"))
    
    print("✅ Done")


if __name__ == "__main__":
    main()
 