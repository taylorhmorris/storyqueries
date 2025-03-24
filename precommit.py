import subprocess

if __name__ == "__main__":
  # Linting / Style checks
  print("Linting / Style checks")
  subprocess.run(["black", "./src", "./tests"])
  subprocess.run(["pylint", "./src", "./tests"])
  subprocess.run(["isort", "./src", "./tests"])
  subprocess.run(["flake8", "./src", "./tests"])  
  
  # Type checks
  print("\nType checks")
  subprocess.run(["mypy", "./src"])
  
  # Security checks
  print("\nSecurity checks")
  subprocess.run(["bandit", "-q", "-r", "./src"])
  
  # Package checks
  print("\nPackage checks")
  subprocess.run(["pyroma", "."])

  # Test coverage
  print("\nTesting and coverage")
  completed = subprocess.run(["coverage", "run", "-m", "pytest", "./tests"])
  if completed.returncode == 0:
    subprocess.run(["coverage", "report", "-m"])
  else:
    print("Coverage report skipped because of failing tests")