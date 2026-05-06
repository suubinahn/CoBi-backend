def detect_language(code: str) -> str:
    code = code.lower()

    # TypeScript / JavaScript
    if "=>" in code or "console.log" in code or "function " in code:
        return "typescript"

    # Python
    if "def " in code or "import " in code or "print(" in code:
        return "python"

    # Java
    if "public class" in code or "system.out.println" in code:
        return "java"

    # C++
    if "#include" in code:
        return "c++"

    return "unknown"