import difflib

# File paths
file1_path = r"D:\2025 Projects\2025-AptiProject\Project-APTI\client\templates\subadmin\add-content\edit-content\edit_content.html"
file2_path = r"D:\2025 Projects\2025-AptiProject\Project-APTI\client\templates\admin\add-content\edit-content\edit_content.html"


# Function to read file content
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


# Read the content of both files
file1_content = read_file(file1_path)
file2_content = read_file(file2_path)

# Use difflib to compare the files
diff = difflib.ndiff(file1_content, file2_content)

# Loop through the differences and print the line number and content
diff_lines = []
for i, line in enumerate(diff):
    if line.startswith("- ") or line.startswith(
        "+ "
    ):  # Differences are marked with - or +
        diff_lines.append(f"Line {i + 1}: {line.strip()}")

# Print the result
if diff_lines:
    print(f"Total differences: {len(diff_lines)}")
    for diff_line in diff_lines:
        print(diff_line)
else:
    print("No differences found.")
