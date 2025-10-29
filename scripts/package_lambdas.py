import os
import shutil
import subprocess
import zipfile
from pathlib import Path

LAMBDA_ROOT = Path('lambda-functions')
LAMBDA_FUNCTIONS = [
    'auth-api',
    'cart-api',
    'products-api',
    'orders-api',
    'inventory-updater',
    'notification-sender',
    'order-processor',
    'payment-processor'
]

for func in LAMBDA_FUNCTIONS:
    func_dir = LAMBDA_ROOT / func
    build_dir = func_dir / 'lambda_build'
    zip_path = func_dir / 'function.zip'

    # Clean old build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Install dependencies
    req_file = func_dir / 'requirements.txt'
    if req_file.exists():
        subprocess.run(['pip', 'install', '-r', str(req_file), '-t', str(build_dir)], check=True)

    # Copy source files
    for py_file in func_dir.glob('*.py'):
        shutil.copy(py_file, build_dir)

    # Zip contents
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = str(file_path.relative_to(build_dir))
                zipf.write(file_path, arcname)

    print(f'Packaged {func} -> {zip_path}')
