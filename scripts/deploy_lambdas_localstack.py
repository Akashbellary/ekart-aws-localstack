import os
import subprocess
from pathlib import Path
import shutil
import traceback

def debug(msg):
    print(f"[deploy_lambdas_localstack] {msg}")

AWLOCALPATH = shutil.which('awslocal') or "awslocal"
REPO_ROOT = Path(__file__).parent.parent.resolve()
LAMBDAROOT = REPO_ROOT / "lambda-functions"
ROLE_ARN = "arn:aws:iam::000000000000:role/lambda-role"

LAMBDACONFIG = [
    {"name": "auth-api", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "cart-api", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "products-api", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "orders-api", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "inventory-updater", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "notification-sender", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "order-processor", "handler": "handler.lambda_handler", "runtime": "python3.10"},
    {"name": "payment-processor", "handler": "handler.lambda_handler", "runtime": "python3.10"},
]

def run_awslocal(args):
    try:
        proc = subprocess.run([AWLOCALPATH] + args, capture_output=True, text=True)
        debug(f"CMD: {' '.join([AWLOCALPATH] + args)}")
        debug("STDOUT:\n" + proc.stdout)
        if proc.stderr:
            debug("STDERR:\n" + proc.stderr)
        return proc
    except Exception as e:
        debug(f"❌ ERROR running awslocal: {e}")
        traceback.print_exc()

def lambda_exists(function_name):
    try:
        proc = run_awslocal(['lambda', 'list-functions'])
        if proc.returncode != 0:
            debug(f"Error listing functions: {proc.stderr}")
            return False
        if function_name in proc.stdout:
            return True
    except Exception:
        pass
    return False

def main():
    debug(f"Checking all Lambda .zip packages in {LAMBDAROOT}")
    for cfg in LAMBDACONFIG:
        name = cfg['name']
        zippath = (LAMBDAROOT / name / "function.zip").resolve()
        handler_name = cfg['handler']
        runtime = cfg['runtime']

        debug(f"\n>>> Deploying {name}")
        if not zippath.exists():
            debug(f"⚠️  ZIP NOT FOUND: {zippath}")
            continue

        try:
            if lambda_exists(name):
                debug(f"Function {name} exists, updating code...")
                proc = run_awslocal([
                    "lambda", "update-function-code",
                    "--function-name", name,
                    "--zip-file", f"fileb://{zippath}"
                ])
                if proc.returncode != 0:
                    debug(f"Update code failed for {name}!")
            else:
                debug(f"Function {name} not found, creating new Lambda...")
                proc = run_awslocal([
                    "lambda", "create-function",
                    "--function-name", name,
                    "--runtime", runtime,
                    "--handler", handler_name,
                    "--zip-file", f"fileb://{zippath}",
                    "--role", ROLE_ARN
                ])
                if proc.returncode != 0:
                    debug(f"Create function failed for {name}!")
            debug(f"Done: {name}")
        except Exception as e:
            debug(f"❌ ERROR deploying {name}: {e}")
            traceback.print_exc()
            continue

    debug("\nAll Lambda functions processed. Check logs for errors above.")

if __name__ == "__main__":
    main()
