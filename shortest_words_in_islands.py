import os
import re

# Folder containing the text files
folder_path = "islands"

results = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt") and filename != "iii.txt":
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
            # Extract words (only alphabetic sequences)
            words = re.findall(r"[A-Za-z]+", text)
            
            if words:
                shortest_word = min(words, key=len)
                results.append((filename, shortest_word, len(shortest_word)))

# Sort by word length (ascending)
results.sort(key=lambda x: x[2])

# Write report
report_path = os.path.join(folder_path, "shortest-word-per-island.txt")
with open(report_path, "w", encoding="utf-8") as report:
    for filename, word, length in results:
        report.write(f"{filename} {word} {length}\n")

print("shortest-word-per-island.txt created successfully.")
