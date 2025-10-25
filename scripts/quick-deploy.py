#!/usr/bin/env python3
"""
Quick Deploy Script - Deploy Everything in One Command
"""
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def run_command(description, command, cwd=None):
    """Run a command and display progress"""
    print(f"\n{'='*70}")
    print(f"🔄 {description}")
    print(f"{'='*70}")
    
    try:
        if isinstance(command, list):
            result = subprocess.run(
                command,
                cwd=cwd or PROJECT_ROOT,
                check=True,
                capture_output=False,
                text=True
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or PROJECT_ROOT,
                check=True,
                capture_output=False,
                text=True
            )
        print(f"✅ {description} - COMPLETED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e}")
        return False

def check_localstack():
    """Check if LocalStack is running"""
    import requests
    try:
        response = requests.get('http://localhost:4566/_localstack/health', timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    """Main quick deploy function"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║          🚀 EKART STORE - SERVERLESS QUICK DEPLOY 🚀            ║
║                                                                  ║
║     Deploying complete serverless infrastructure to LocalStack  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if LocalStack is running
    print("\n🔍 Checking LocalStack status...")
    if not check_localstack():
        print("\n⚠️  LocalStack is not running!")
        print("\nPlease start LocalStack first:")
        print("  docker-compose up localstack")
        print("\nThen wait 15-20 seconds and run this script again.")
        sys.exit(1)
    
    print("✅ LocalStack is running!")
    
    # Deploy serverless infrastructure
    if not run_command(
        "Deploying Serverless Infrastructure (DynamoDB, Cognito, S3, Lambda, API Gateway)",
        [sys.executable, str(PROJECT_ROOT / 'scripts' / 'deploy-serverless.py')]
    ):
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)
    
    # Seed database
    seed_script = PROJECT_ROOT / 'scripts' / 'seed-products-fixed.py'
    if not seed_script.exists():
        seed_script = PROJECT_ROOT / 'scripts' / 'seed-data.py'
    
    if not run_command(
        "Seeding Database with Products",
        [sys.executable, str(seed_script)]
    ):
        print("\n⚠️  Database seeding failed, but infrastructure is deployed.")
    
    # Configure frontend
    if not run_command(
        "Configuring Frontend Environment",
        [sys.executable, str(PROJECT_ROOT / 'scripts' / 'configure-frontend.py')]
    ):
        print("\n⚠️  Frontend configuration failed. You may need to configure manually.")
    
    # Success message
    print(f"\n{'='*70}")
    print("✅ DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}\n")
    
    # Read config for URLs
    try:
        import json
        config_path = PROJECT_ROOT / 'serverless-config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            print("📋 DEPLOYMENT SUMMARY:")
            print(f"  • API Gateway URL: {config.get('api_url', 'N/A')}")
            print(f"  • User Pool ID: {config.get('user_pool_id', 'N/A')}")
            print(f"  • Client ID: {config.get('client_id', 'N/A')}")
    except:
        pass
    
    print("\n🎯 NEXT STEPS:")
    print("  1. Start frontend:")
    print("     cd frontend")
    print("     npm run dev")
    print()
    print("  2. Open application:")
    print("     http://localhost:3000")
    print()
    print("  3. (Optional) Test API:")
    print("     Check serverless-config.json for API URL")
    print()
    print("📚 For more information, see:")
    print("  • COMMANDS_SERVERLESS.md - Complete command reference")
    print("  • SERVERLESS_README.md - Architecture guide")
    print("  • SERVERLESS_MIGRATION_SUMMARY.md - What changed")
    print()
    print("🎉 Happy coding!")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Deployment cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
