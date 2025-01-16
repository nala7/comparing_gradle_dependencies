import json
import subprocess
import re
import os


def run_gradle_dependencies(file_path):
    try:
        os.chdir(file_path)
        result = subprocess.run(
            ["./gradlew", "dependencies"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print("Error running gradle dependencies:", result.stderr)
            return None

        output_file = "gradle_dependencies_output.txt"
        with open(output_file, "w") as f:
            f.write(result.stdout)

        print(f"Output saved to {output_file}")

        return result.stdout
    except FileNotFoundError:
        print("Gradle is not installed or not found in PATH.")
        return None

def parse_dependency_line(line):
    pattern = r".*[\+\\]---\s*(.*)"

    match = re.match(pattern, line)
    if match:
        content = match.group(1)
        pattern =pattern = r":|->"
        parts = re.split(pattern, content)
        if '->' in parts:
            idx = parts.index('->')
            return parts[0], parts[1], parts[idx + 1]
        elif len(parts) == 3:
            return parts[0], parts[1], parts[2]

    return None

def parse_dependencies(lines, level=0):
    result = []
    while lines:
        line = lines[0]
        matched = parse_dependency_line(line)
        if matched:
            group_id, artifact_id, version = matched
            version = version.split()[0]
            result.append({
                "groupId": group_id,
                "artifactId": artifact_id,
                "version": version
            })
        lines.pop(0)
    return result

def parse_gradle_output(input_text):
    lines = input_text.strip().split("\n")
    dependencies = parse_dependencies(lines)
    return dependencies

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename


def gradle_to_json(file_path):
    output = run_gradle_dependencies(file_path)
    if output:
        parsed_dependencies = parse_gradle_output(output)
        json_path = save_to_json(parsed_dependencies, "dependencies.json")
        print("Dependencies have been saved to dependencies.json.")
        return parsed_dependencies
