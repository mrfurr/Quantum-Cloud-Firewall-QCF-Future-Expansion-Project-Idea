import os
import sys

def check_python_syntax(filepath):
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        compile(source, filepath, 'exec')
        print(f"✅ {filepath}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {filepath}: Syntax Error - {e}")
        return False
    except Exception as e:
        print(f"⚠️  {filepath}: Could not check - {e}")
        return False

# Check all Python files
python_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and 'check_syntax' not in file:
            python_files.append(os.path.join(root, file))

print("Checking Python files for syntax errors...")
issues = []
for file in python_files:
    if not check_python_syntax(file):
        issues.append(file)

if issues:
    print(f"\n🚨 Found {len(issues)} files with syntax errors:")
    for issue in issues:
        print(f"   - {issue}")
else:
    print("\n🎉 All files have correct syntax!")
