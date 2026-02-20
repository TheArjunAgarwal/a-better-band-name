import string

class WordLadder:
    def __init__(self, dictionary_path):
        with open(dictionary_path, 'r') as f:
            self.words = {line.strip().lower() for line in f if line.strip()}

    def get_dist1_words(self, word, use_swap=True, use_insert=True, use_delete=True):
        """Return all distance-1 words (first BFS layer)."""
        if word not in self.words:
            return set()

        neighbors = set()
        alphabet = string.ascii_lowercase
        L = len(word)

        # 1. Replace one letter
        for i in range(L):
            for c in alphabet:
                if c != word[i]:
                    candidate = word[:i] + c + word[i+1:]
                    if candidate in self.words:
                        neighbors.add(candidate)

        # 2. Swap adjacent letters
        if use_swap:
            for i in range(L - 1):
                if word[i] != word[i+1]:
                    swapped = (
                        word[:i] +
                        word[i+1] +
                        word[i] +
                        word[i+2:]
                    )
                    if swapped in self.words:
                        neighbors.add(swapped)

        # 3. Insert one letter
        if use_insert:
            for i in range(L + 1):
                for c in alphabet:
                    candidate = word[:i] + c + word[i:]
                    if candidate in self.words:
                        neighbors.add(candidate)

        # 4. Delete one letter
        if use_delete:
            for i in range(L):
                candidate = word[:i] + word[i+1:]
                if candidate in self.words:
                    neighbors.add(candidate)

        return neighbors

ladder = WordLadder("dictionary.txt")
print(ladder.get_dist1_words("kitten"))
