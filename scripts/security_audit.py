import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
FRONTEND = ROOT / "frontend"
errors: list[str] = []


def report(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def python_files(directory: Path):
    return (path for path in directory.rglob("*.py") if ".venv" not in path.parts and "__pycache__" not in path.parts)


def main() -> int:
    sql_files = list((BACKEND / "sql").glob("*.sql"))
    sql_text = "\n".join(path.read_text(encoding="utf-8") for path in sql_files)
    report(not re.search(r"\bpassword\s+TEXT\b", sql_text, re.IGNORECASE), "Found a plaintext password column")

    for path in python_files(BACKEND):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as error:
            errors.append(f"Python syntax error in {path.relative_to(ROOT)}: {error}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"execute", "execute_query", "execute_returning"}:
                report(not node.args or not isinstance(node.args[0], ast.JoinedStr), f"Interpolated SQL in {path.relative_to(ROOT)}")

    route_functions_without_dependency = []
    for path in BACKEND.rglob("routes.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            is_route = any(
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and decorator.func.attr in {"get", "post", "put", "patch", "delete"}
                for decorator in node.decorator_list
            )
            is_public = node.name in {"register", "login"}
            has_dependency = any(
                isinstance(default, ast.Call)
                and isinstance(default.func, ast.Name)
                and default.func.id == "Depends"
                for default in node.args.defaults + node.args.kw_defaults
                if default is not None
            )
            if is_route and not is_public and not has_dependency:
                route_functions_without_dependency.append(f"{path.relative_to(ROOT)}:{node.name}")
    report(not route_functions_without_dependency, f"Protected routes lack Depends: {route_functions_without_dependency}")

    main_source = (BACKEND / "main.py").read_text(encoding="utf-8")
    report("allow_origins=[settings.frontend_origin]" in main_source, "CORS origin is not restricted to the configured frontend")
    frontend_source = "\n".join(path.read_text(encoding="utf-8") for suffix in ("*.js", "*.jsx") for path in FRONTEND.rglob(suffix) if "node_modules" not in path.parts)
    report("Bearer ${token}" in frontend_source, "Frontend does not attach a Bearer token")
    service_worker = (FRONTEND / "public" / "sw.js").read_text(encoding="utf-8")
    report("pathname.startsWith('/api/')" in service_worker, "Service worker does not bypass API requests")
    ignore_check = subprocess.run(["git", "check-ignore", "-q", "backend/.env"], cwd=ROOT, check=False)
    report(ignore_check.returncode == 0, "backend/.env is not ignored by git")
    report("diagnoses" not in frontend_source.lower() and "cures" not in frontend_source.lower(), "Frontend contains a diagnostic/treatment claim")
    report(not (ROOT / "smritisaathi.db").exists() and not (BACKEND / "smritisaathi.db").exists(), "A legacy database file remains")

    if errors:
        print("Security audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Security audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())