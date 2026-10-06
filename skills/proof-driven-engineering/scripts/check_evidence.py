import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


def validate(record: object, root: Path) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ["Record must be an object"]
    if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        errors.append("schema_version must be integer 1")
    if not isinstance(record.get("goal"), str) or not record["goal"].strip():
        errors.append("A current goal is required")
    root = Path(root).resolve()
    checks = record.get("checks")
    requirements = record.get("requirements")
    if not isinstance(checks, list) or not checks:
        return errors + ["At least one check is required"]
    if not isinstance(requirements, list) or not requirements:
        return errors + ["At least one requirement is required"]
    check_ids = set()
    for check in checks:
        if not isinstance(check, dict):
            errors.append("Each check must be an object")
            continue
        check_id = check.get("id")
        if not isinstance(check_id, str) or not check_id.strip():
            errors.append("Each check needs a nonempty id")
            continue
        if check_id in check_ids:
            errors.append(f"Duplicate check id: {check_id}")
        check_ids.add(check_id)
        if check.get("status") != "pass":
            errors.append(f"{check_id}: check is not recorded as passing")
        if type(check.get("exit_code")) is not int or check["exit_code"] != 0:
            errors.append(f"{check_id}: pass requires integer exit_code 0")
        if not isinstance(check.get("command"), str) or not check["command"].strip():
            errors.append(f"{check_id}: actual command is required")
        inputs = check.get("inputs")
        if not isinstance(inputs, dict) or not inputs:
            errors.append(f"{check_id}: input hashes are required")
            continue
        for name, digest in inputs.items():
            if not isinstance(name, str) or not name or "\\" in name or ":" in name:
                errors.append(f"{check_id}: input path must be relative POSIX text")
                continue
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or "\x00" in name:
                errors.append(f"{check_id}: unsafe input path")
                continue
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"{check_id}: malformed SHA-256")
                continue
            try:
                source = (root / path).resolve()
                if not source.is_relative_to(root):
                    errors.append(f"{check_id}: input escapes the root")
                    continue
                if not source.is_file():
                    errors.append(f"{check_id}: input must be a regular file")
                    continue
                with source.open("rb") as stream:
                    current = hashlib.file_digest(stream, "sha256").hexdigest()
            except (OSError, ValueError, RuntimeError) as exc:
                errors.append(f"{check_id}: input unreadable ({type(exc).__name__})")
                continue
            if current != digest:
                errors.append(f"{check_id}: input changed; rerun affected verification")
    requirement_ids = set()
    for requirement in requirements:
        if not isinstance(requirement, dict):
            errors.append("Each requirement must be an object")
            continue
        requirement_id = requirement.get("id")
        if not isinstance(requirement_id, str) or not requirement_id.strip():
            errors.append("Each requirement needs a nonempty id")
            continue
        if requirement_id in requirement_ids:
            errors.append(f"Duplicate requirement id: {requirement_id}")
        requirement_ids.add(requirement_id)
        references = requirement.get("checks")
        if not isinstance(references, list) or not references:
            errors.append(f"{requirement_id}: acceptance checks are required")
            continue
        for reference in references:
            if not isinstance(reference, str) or reference not in check_ids:
                errors.append(f"{requirement_id}: acceptance check is missing")
    return errors


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError("Nonstandard JSON constant")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check recorded coverage and input freshness")
    parser.add_argument("record", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        with args.record.open(encoding="utf-8") as stream:
            record = json.load(stream, object_pairs_hook=unique_object, parse_constant=reject_constant)
        errors = validate(record, args.root)
    except (OSError, ValueError, RecursionError) as exc:
        print(f"Evidence record unavailable or invalid ({type(exc).__name__})", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Recorded coverage and current input hashes validated; command execution is not attested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
