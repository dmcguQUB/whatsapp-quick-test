"""
Minimal WSGI entry point for Railway debugging
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 50)
print("WSGI: Starting app initialization")
print("=" * 50)

try:
    from src.app import create_app
    print("WSGI: Imported create_app successfully")

    app = create_app()
    print("WSGI: App created successfully")
    print(f"WSGI: App instance: {app}")
    print(f"WSGI: Routes: {[rule.rule for rule in app.url_map.iter_rules()]}")
    print("=" * 50)

except Exception as e:
    print("=" * 50)
    print(f"WSGI: ERROR during app creation: {e}")
    import traceback
    traceback.print_exc()
    print("=" * 50)
    raise
