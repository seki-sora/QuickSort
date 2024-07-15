import os
import re


def organize_files(directory, similarity_threshold=0.8):
    """
  Organizes files in a directory based on similar names.

  Args:
      directory (str): The path to the directory containing the files.
      similarity_threshold (float, optional): The minimum similarity score
          required to consider names similar (defaults to 0.8). Valid values
          are between 0.0 (no similarity) and 1.0 (exact match).
  """

    for filename in os.listdir(directory):
        # Extract base name and optional extension (using a more robust regex)
        match = re.search(r"(.*?)(?:\.(\w+))?$", filename)
        if match:
            base_name, extension = match.groups()
        else:
            base_name, extension = filename, None

        # Identify similar names using Levenshtein distance for string similarity
        similar_files = []
        for other_filename in os.listdir(directory):
            if other_filename != filename:
                other_match = re.search(r"(.*?)(?:\.(\w+))?$", other_filename)
                if other_match:
                    other_base_name, _ = other_match.groups()
                    similarity = _calculate_similarity(base_name, other_base_name)
                    if similarity >= similarity_threshold:
                        similar_files.append(other_filename)

        # Create a folder with a descriptive name (avoid duplicates)
        if similar_files:
            folder_name = f"{base_name} (and {len(similar_files) + 1} similar)"
            count = 1
            while os.path.exists(os.path.join(directory, folder_name)):
                folder_name = f"{base_name} (and {len(similar_files) + count} similar)"
                count += 1
            os.makedirs(os.path.join(directory, folder_name))

            # Move files to the created folder
            for similar_file in similar_files:
                os.rename(os.path.join(directory, similar_file), os.path.join(directory, folder_name, similar_file))
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, folder_name, filename))  # Move the original file too


def _calculate_similarity(str1, str2):
    """
  Calculates the Levenshtein distance between two strings (similarity metric).

  Args:
      str1 (str): The first string.
      str2 (str): The second string.

  Returns:
      float: The Levenshtein similarity score between 0.0 (no similarity)
          and 1.0 (exact match).
  """
    m = len(str1) + 1
    n = len(str2) + 1
    dp = [[0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        dp[i][0] = i

    for j in range(n):
        dp[0][j] = j

    for i in range(1, m):
        for j in range(1, n):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)

    # Calculate similarity based on Levenshtein distance (higher is more similar)
    similarity = 1 - (dp[m - 1][n - 1] / (max(m, n)))
    return similarity


if __name__ == "__main__":
    directory = os.getcwd()  # Replace with your actual directory path
    similarity_threshold = 0.8  # Adjust this value for desired similarity level (0.0 to 1.0)
    organize_files(directory, similarity_threshold)
    print("Files organized successfully!")
