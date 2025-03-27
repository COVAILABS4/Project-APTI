import subprocess

# Define the two commit IDs
commit1 = "fac3cd9b55de563c4a5ba42dc5ae66ac7b3569a0"
commit2 = "64a6df75b9142dd1f7abe984eb347b1eb47061fa"

try:
    # Run 'git diff' to get the status of changed files
    result = subprocess.run(
        ["git", "diff", "--name-status", commit1, commit2],
        capture_output=True,
        text=True,
        check=True,
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

    # Write the categorized file names to 'changed_files.txt'
    with open("changed_files.txt", "w") as file:
        file.write("Updated Files:\n")
        file.write("\n".join(updated_files) + "\n\n")
        file.write("Newly Created Files:\n")
        file.write("\n".join(new_files) + "\n\n")
        file.write("Deleted Files:\n")
        file.write("\n".join(deleted_files) + "\n\n")
        print("Categorized file names have been written to 'changed_files.txt'")

except subprocess.CalledProcessError as e:
    print(f"Error running git diff: {e}")
