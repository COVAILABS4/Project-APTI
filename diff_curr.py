import subprocess

# Define the two commit IDs
commit1 = "64a6df75b9142dd1f7abe984eb347b1eb47061fa"
commit2 = "930c2b3a3ae286e0968841c72df19a535076c639"

try:
    # Run 'git diff' to get the status of changed files
    result = subprocess.run(
        ["git", "diff", "--name-status", commit1, commit2],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",  # Fix for UnicodeDecodeError
    )

    # Initialize lists for different file change types
    updated_files = []
    new_files = []
    deleted_files = []

    # Parse the output
    for line in result.stdout.splitlines():
        status, file_path = line.split("\t", 1)

        # Exclude files in migrations, .pyc files, cache dirs, and .jpg files except 'krishtec.jpg'
        if (
            file_path.endswith(".pyc")
            or "__pycache__" in file_path
            or "migrations/" in file_path
            or (
                file_path.startswith("media/")
                and file_path.endswith(".jpg")
                and "krishtec.jpg" not in file_path
            )
        ):
            continue

        if status == "M":
            updated_files.append(file_path)
        elif status == "A":
            new_files.append(file_path)
        elif status == "D":
            deleted_files.append(file_path)

    # Write the categorized file names and modified lines to 'changed_files.txt'
    with open("changed_files.txt", "w", encoding="utf-8") as file:
        file.write("Updated Files (with modified lines and line numbers):\n")
        for updated_file in updated_files:
            file.write(f"\nFile Name: {updated_file}\n")
            # Run git diff to get the modified lines for the updated file
            diff_result = subprocess.run(
                ["git", "diff", "-U0", commit1, commit2, "--", updated_file],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",  # Fix for UnicodeDecodeError
            )

            # Check if diff_result.stdout is not None before processing
            if diff_result.stdout:
                prev_line_number = None
                updated_line_number = None

                for line in diff_result.stdout.splitlines():
                    if line.startswith("@@"):  # Line number section from the diff
                        parts = line.split()
                        prev_line_number = int(
                            parts[1].split(",")[0][1:]
                        )  # Original file line number
                        updated_line_number = int(
                            parts[2].split(",")[0][1:]
                        )  # New file line number
                    elif line.startswith("-") and prev_line_number is not None:
                        file.write(
                            f"Line {prev_line_number}: {line[1:].strip()} (Previous)\n"
                        )
                        prev_line_number += 1
                    elif line.startswith("+") and updated_line_number is not None:
                        file.write(
                            f"Line {updated_line_number}: {line[1:].strip()} (Updated)\n"
                        )
                        updated_line_number += 1

        file.write("\nNewly Created Files:\n")
        for new_file in new_files:
            file.write(f"File Name: {new_file}\n")

        file.write("\nDeleted Files:\n")
        for deleted_file in deleted_files:
            file.write(f"File Name: {deleted_file}\n")

    print(
        "Updated lines, file names, and categorized files have been written to 'changed_files.txt'"
    )

except subprocess.CalledProcessError as e:
    print(f"Error running git diff: {e}")
