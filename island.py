import collections
import os
import time
from tqdm import tqdm

class IslandSolver:
    def __init__(self, dictionary_path, ops=(False, True, True)):
        self.words = set()
        self.ops = ops 
        
        if not os.path.exists(dictionary_path):
            print(f"Error: {dictionary_path} not found.")
            return
            
        print(f"Loaded {len(self.words)} words. Building adjacency list...")
        self.adj = self._build_full_adj()

    def _build_full_adj(self):
        adj = collections.defaultdict(set)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        
        buckets = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                template = word[:i] + "_" + word[i+1:]
                buckets[template].append(word)
        for words_in_bucket in buckets.values():
            for w1 in words_in_bucket:
                for w2 in words_in_bucket:
                    if w1 != w2: adj[w1].add(w2)

        use_swap, use_ins, use_del = self.ops
        for word in self.words:
            if use_swap:
                chars = list(word)
                for i in range(len(chars) - 1):
                    chars[i], chars[i+1] = chars[i+1], chars[i]
                    swapped = "".join(chars)
                    if swapped in self.words and swapped != word: adj[word].add(swapped)
                    chars[i], chars[i+1] = chars[i+1], chars[i]
            if use_ins:
                for i in range(len(word) + 1):
                    for char in alphabet:
                        new_w = word[:i] + char + word[i:]
                        if new_w in self.words and new_w != word: adj[word].add(new_w)
            if use_del:
                for i in range(len(word)):
                    new_w = word[:i] + word[i+1:]
                    if new_w in self.words and new_w != word: adj[word].add(new_w)
        return adj

    def find_islands(self):
        visited = set()
        islands = []
        for word in self.words:
            if word not in visited:
                component = []
                queue = collections.deque([word])
                visited.add(word)
                while queue:
                    curr = queue.popleft()
                    component.append(curr)
                    for neighbor in self.adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                # Keep islands with 2 or more words
                if len(component) >= 2:
                    islands.append(component)
        return islands

    def get_island_diameter(self, island, timeout_seconds=3000):
        max_d = 0
        furthest_pair = (None, None)
        start_time = time.time()
        
        pbar = tqdm(island, desc="Calculating Diameter", leave=False)
        
        for start_node in pbar:
            if time.time() - start_time > timeout_seconds:
                pbar.set_postfix({"status": "TIMEOUT"})
                return "TIMEOUT", (None, None)

            distances = {start_node: 0}
            queue = collections.deque([start_node])
            
            while queue:
                curr = queue.popleft()
                d = distances[curr]
                if d > max_d:
                    max_d = d
                    furthest_pair = (start_node, curr)
                
                for neighbor in self.adj[curr]:
                    if neighbor not in distances:
                        distances[neighbor] = d + 1
                        queue.append(neighbor)
        return max_d, furthest_pair

def main():
    ISLAND_TIMEOUT = 300000 # Roughly 3 days, meant to just be a placeholder as I originally kept it at 5 mins. 
    REPORT_FILE = "island_report.txt"
    
    solver = IslandSolver('dictionary.txt')
    if not hasattr(solver, 'words'): return
    
    islands = solver.find_islands()
    
    if not os.path.exists('islands'):
        os.makedirs('islands')

    print(f"Found {len(islands)} islands. Analyzing diameters...")
    
    results = []
    for i, island in enumerate(islands):
        filename = f"islands/island_{i+1}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(island))
            
        print(f"\nIsland {i+1}/{len(islands)} (Size: {len(island)})")
        diameter, pair = solver.get_island_diameter(island, timeout_seconds=ISLAND_TIMEOUT)
        
        if diameter == "TIMEOUT":
            results.append((len(island), ">???", ("N/A", "N/A"), f"{filename} (Incomplete)"))
        else:
            results.append((len(island), diameter, pair, filename))

    # Sort results by size descending
    results.sort(key=lambda x: x[0], reverse=True)

    # Formatting the file
    header = f"{'Island File':<30} | {'Size':<6} | {'Diameter':<10} | {'Furthest Pair'}"
    separator = "-" * 85

    with open(REPORT_FILE, 'w', encoding='utf-8') as rf:
        rf.write("ISLAND DIAMETER REPORT\n")
        rf.write(f"Generated on: {time.ctime()}\n")
        rf.write(separator + "\n")
        rf.write(header + "\n")
        rf.write(separator + "\n")
        
        for size, diam, pair, fname in results:
            pair_str = f"{pair[0]} <-> {pair[1]}" if pair[0] else "N/A"
            row = f"{fname:<30} | {size:<6} | {diam:<10} | {pair_str}"
            rf.write(row + "\n")
            print(row)

    print(f"\nFull report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()