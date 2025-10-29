import os
import shutil
import subprocess
import traceback
from pathlib import Path
import zipfile

def debug(msg):
    print(f"[package_all_lambdas] {msg}")

try:
    repo_root = Path(__file__).parent.parent.resolve()
    LAMBDAROOT = repo_root / "lambda-functions"

    debug(f"Packaging Lambdas found at {LAMBDAROOT}")

    if not LAMBDAROOT.is_dir():
        raise FileNotFoundError(f"Lambda root not found: {LAMBDAROOT}")

    for funcdir in LAMBDAROOT.iterdir():
        if not funcdir.is_dir() or funcdir.name.startswith("__"):
            continue
        builddir = funcdir / "build"
        zippath = funcdir / "function.zip"
        handler = funcdir / "handler.py"
        requirements = funcdir / "requirements.txt"

        debug(f"\nPackaging {funcdir.name}")
        if builddir.exists():
            shutil.rmtree(builddir)
            debug(" - Removed old build dir")
        if zippath.exists():
            zippath.unlink()
            debug(" - Removed old zip")

        builddir.mkdir()
        debug(" - Created new build dir")

        has_handler = handler.exists()
        has_requirements = requirements.exists()
        debug(f" - handler.py found: {has_handler}, requirements.txt found: {has_requirements}")

        if has_handler:
            shutil.copy(handler, builddir / handler.name)
        else:
            debug(" ! ERROR: handler.py missing, skipping lambda")
            continue

        for pyfile in funcdir.glob("*.py"):
            if pyfile.name != "handler.py":
                shutil.copy(pyfile, builddir / pyfile.name)
                debug(f" - Copied {pyfile.name}")

        if has_requirements:
            debug(" - Installing dependencies")
            try:
                proc = subprocess.run(
                    ["pip", "install", "-r", str(requirements), "-t", str(builddir)],
                    capture_output=True, text=True
                )
                debug(proc.stdout)
                if proc.returncode != 0:
                    debug(f" ! pip install error: {proc.stderr}")
                    continue
            except Exception as e:
                debug(f" ! ERROR installing dependencies: {e}")
                traceback.print_exc()
                continue

        debug(" - Zipping build folder → function.zip")
        try:
            with zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(builddir):
                    for file in files:
                        full_path = Path(root) / file
                        zipf.write(full_path, full_path.relative_to(builddir))
            debug(f" - Created {zippath}")
        except Exception as e:
            debug(f" ! ERROR zipping build: {e}")
            traceback.print_exc()
            continue

        shutil.rmtree(builddir)
        debug(" - Cleaned up build dir")
    debug("\nPackaging complete.")
except Exception as e:
    debug(f"[FATAL] Unexpected error: {e}")
    traceback.print_exc()
