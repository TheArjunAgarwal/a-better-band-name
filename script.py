import collections

class WordLadder:
    def __init__(self, dictionary_path, extra_words=None):
        self.words = set()
     
        with open(dictionary_path, 'r') as f:
            for line in f:
                word = line.strip().lower()
                if word: self.words.add(word)
        
        if extra_words:
            for word in extra_words:
                self.words.add(word.lower())
        
        print(f"Preprocessing {len(self.words)} words...")
        self.graph_replace = self._build_replace_graph()
        self.graph_swap = self._build_swap_graph()
        self.graph_insert = self._build_insert_graph()
        self.graph_delete = self._build_delete_graph()

    def _get_neighbors(self, word, use_swap, use_insert, use_delete):
        neighbors = set(self.graph_replace.get(word, []))
        if use_swap: neighbors.update(self.graph_swap.get(word, []))
        if use_insert: neighbors.update(self.graph_insert.get(word, []))
        if use_delete: neighbors.update(self.graph_delete.get(word, []))
        return neighbors

    def _build_replace_graph(self):
        adj = collections.defaultdict(list); buckets = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                template = word[:i] + "_" + word[i+1:]; buckets[template].append(word)
        for template in buckets:
            for w1 in buckets[template]:
                for w2 in buckets[template]:
                    if w1 != w2: adj[w1].append(w2)
        return adj

    def _build_swap_graph(self):
        adj = collections.defaultdict(list)
        for word in self.words:
            chars = list(word)
            for i in range(len(chars) - 1):
                chars[i], chars[i+1] = chars[i+1], chars[i]
                swapped = "".join(chars)
                if swapped in self.words and swapped != word: adj[word].append(swapped)
                chars[i], chars[i+1] = chars[i+1], chars[i]
        return adj

    def _build_insert_graph(self):
        adj = collections.defaultdict(list); alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for word in self.words:
            for i in range(len(word) + 1):
                for char in alphabet:
                    new_word = word[:i] + char + word[i:]
                    if new_word in self.words: adj[word].append(new_word)
        return adj

    def _build_delete_graph(self):
        adj = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                new_word = word[:i] + word[i+1:]
                if new_word in self.words: adj[word].append(new_word)
        return adj

    def find_path(self, start, end, use_swap, use_insert, use_delete):
        # Shortest path BFS.
        if start not in self.words or end not in self.words: return None
        queue = collections.deque([(start, [start])])
        visited = {start}
        while queue:
            curr, path = queue.popleft()
            if curr == end: return path
            for n in self._get_neighbors(curr, use_swap, use_insert, use_delete):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))
        return None

    def find_all_furthest_from(self, start, use_swap, use_insert, use_delete):
        #  Finds all words at the maximum reachable distance from 'start'.
        
        if start not in self.words: return [], 0
        
        queue = collections.deque([(start, 0)])
        visited = {start: 0}
        max_dist = 0
        distances = collections.defaultdict(list)

        while queue:
            curr, dist = queue.popleft()
            if dist >= max_dist:
                max_dist = dist
                distances[dist].append(curr)

            for n in self._get_neighbors(curr, use_swap, use_insert, use_delete):
                if n not in visited:
                    visited[n] = dist + 1
                    queue.append((n, dist + 1))
        
        return distances[max_dist], max_dist


vices = [
    "Whiskey", "Beer", "Wine", "Vodka", "Rum", "Gin", "Tequila", "Brandy",
    "Nicotine", "Ganja", "LSD", "Coke", "Heroin", "Morphine", "Hash",
    "Caffeine", "Tobacco", "Cigar", "Bong", "Adderall", "Xanax", "Absinthe",
    "Algorithms", "Python", "Coding", "Java", "Binary", "Debug", "Linux", "Matrix", "Haskell"
]

engine = WordLadder('dictionary.txt', extra_words=vices)
ops = (False, True, True) 

# Furthest from Sex
furthest_words, dist = engine.find_all_furthest_from("sex", *ops)
print("\n" + "="*40)
print(f"--- EQUALLY DISTANT FROM 'SEX' ({dist} steps) ---")
print(f"Found {len(furthest_words)} words. Here are some top picks:")
for w in furthest_words[:10]:
    print(f" - {w.capitalize()} After Sex")
if len(furthest_words) > 10: print(f" ... and {len(furthest_words)-10} more.")


# The Vice Ladder
print("\n" + "="*40)
print("--- THE VICE LADDER ---")
results = []
for item in vices:
    path = engine.find_path("sex", item.lower(), *ops)
    if path: results.append((len(path), path))

results.sort()
for length, path in results:
    print(f"[{length} steps] {path[-1].capitalize()} After Sex | {' -> '.join(path)}")