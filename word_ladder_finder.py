import collections

class WordLadder:
    def __init__(self, dictionary_path):
        self.words = set()
        with open(dictionary_path, 'r') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.words.add(word)
        
        # Pre-process graphs
        print("Preprocessing graphs... this may take a moment.")
        self.graph_replace = self._build_replace_graph()
        self.graph_swap = self._build_swap_graph()
        self.graph_insert = self._build_insert_graph()
        self.graph_delete = self._build_delete_graph()
        print("Preprocessing complete.")

    def _build_replace_graph(self):
        # Standard word ladder: change one letter.
        adj = collections.defaultdict(list)
        buckets = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                template = word[:i] + "_" + word[i+1:]
                buckets[template].append(word)
        for template in buckets:
            for w1 in buckets[template]:
                for w2 in buckets[template]:
                    if w1 != w2:
                        adj[w1].append(w2)
        return adj

    def _build_swap_graph(self):
        # Swap two adjacent letters.
        adj = collections.defaultdict(list)
        for word in self.words:
            chars = list(word)
            for i in range(len(chars) - 1):
                chars[i], chars[i+1] = chars[i+1], chars[i]
                swapped = "".join(chars)
                if swapped in self.words and swapped != word:
                    adj[word].append(swapped)
                # Swap back for next iteration
                chars[i], chars[i+1] = chars[i+1], chars[i]
        return adj

    def _build_insert_graph(self):
        # Add one letter to increase length.
        adj = collections.defaultdict(list)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for word in self.words:
            for i in range(len(word) + 1):
                for char in alphabet:
                    new_word = word[:i] + char + word[i:]
                    if new_word in self.words:
                        adj[word].append(new_word)
        return adj

    def _build_delete_graph(self):
        # Remove one letter to decrease length
        adj = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                new_word = word[:i] + word[i+1:]
                if new_word in self.words:
                    adj[word].append(new_word)
        return adj

    def find_ladder(self, start, end, use_swap, use_insert, use_delete):
        if start not in self.words or end not in self.words:
            return "One or both words not in dictionary."
        
        # Combine graphs based on user choice
        queue = collections.deque([(start, [start])])
        visited = {start}

        while queue:
            current_word, path = queue.popleft()
            if current_word == end:
                return " -> ".join(path)

            # Gather all possible neighbors based on enabled rules
            neighbors = set(self.graph_replace.get(current_word, []))
            if use_swap:
                neighbors.update(self.graph_swap.get(current_word, []))
            if use_insert:
                neighbors.update(self.graph_insert.get(current_word, []))
            if use_delete:
                neighbors.update(self.graph_delete.get(current_word, []))

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return "No path found."

ladder_engine = WordLadder('dictionary.txt')

while True:
    print("\n--- Word Ladder Solver ---")
    start = input("Start word: ").strip().lower()
    if not start: break
    end = input("End word:   ").strip().lower()
    
    swap = input("Enable Swapping? (y/n): ").lower() == 'y'
    ins = input("Enable Insertion? (y/n): ").lower() == 'y'
    dele = input("Enable Deletion? (y/n): ").lower() == 'y'

    result = ladder_engine.find_ladder(start, end, swap, ins, dele)
    print(f"\nResult: {result}")
    
    if input("\nTry another? (y/n): ").lower() != 'y':
        break