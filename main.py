from argparse import ArgumentParser
from pathlib import Path

from PIL import Image
import pillow_heif


def convert_heic_folder(input_dir: Path) -> None:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a folder: {input_dir}")

    heic_files = []

    for path in input_dir.iterdir():
        if path.is_file() and path.suffix.lower() == ".heic":
            heic_files.append(path)

    if not heic_files:
        print("No HEIC files found.")
        return

    for heic_path in heic_files:
        print(f"🔄 Converting {heic_path.name}...")

        png_path = heic_path.with_suffix(".png")
        heif_file = pillow_heif.read_heif(heic_path)

        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )

        image.save(png_path, format="PNG")

        # Only delete source after PNG was successfully saved
        heic_path.unlink()

        print(f"✅ Replaced {heic_path.name} with {png_path.name}")

    print("✅ Done")


def main() -> None:
    parser = ArgumentParser(
        description="Convert HEIC files in a folder to PNG and remove the originals."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to the folder containing HEIC files",
    )

    args = parser.parse_args()
    convert_heic_folder(args.input_dir)


if __name__ == "__main__":
    main()