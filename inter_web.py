import streamlit as st
import collections
import os

class WordLadder:
    def __init__(self, words_list):
        self.words = set(words_list)
        self.adj_replace = self._build_replace_graph()
        self.adj_swap = self._build_swap_graph()
        self.adj_insert = self._build_insert_graph()
        self.adj_delete = self._build_delete_graph()

    def _build_replace_graph(self):
        adj = collections.defaultdict(set)
        buckets = collections.defaultdict(list)
        for word in self.words:
            for i in range(len(word)):
                template = word[:i] + "_" + word[i+1:]
                buckets[template].append(word)
        for words in buckets.values():
            for w1 in words:
                for w2 in words:
                    if w1 != w2: adj[w1].add(w2)
        return adj

    def _build_swap_graph(self):
        adj = collections.defaultdict(set)
        for word in self.words:
            chars = list(word)
            for i in range(len(chars) - 1):
                chars[i], chars[i+1] = chars[i+1], chars[i]
                sw = "".join(chars)
                if sw in self.words and sw != word: adj[word].add(sw)
                chars[i], chars[i+1] = chars[i+1], chars[i]
        return adj

    def _build_insert_graph(self):
        adj = collections.defaultdict(set)
        for word in self.words:
            for i in range(len(word) + 1):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    new_w = word[:i] + char + word[i:]
                    if new_w in self.words and new_w != word: adj[word].add(new_w)
        return adj

    def _build_delete_graph(self):
        adj = collections.defaultdict(set)
        for word in self.words:
            for i in range(len(word)):
                new_w = word[:i] + word[i+1:]
                if new_w in self.words and new_w != word: adj[word].add(new_w)
        return adj

    def get_neighbors(self, word, ops):
        n = set(self.adj_replace.get(word, []))
        if ops['swap']: n.update(self.adj_swap.get(word, []))
        if ops['ins']: n.update(self.adj_insert.get(word, []))
        if ops['del']: n.update(self.adj_delete.get(word, []))
        return sorted(list(n))

    def find_shortest(self, start, end, ops):
        queue = collections.deque([(start, [start])])
        visited = {start}
        while queue:
            curr, path = queue.popleft()
            if curr == end: return path
            for neighbor in self.get_neighbors(curr, ops):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

# --- STREAMLIT UI ---
st.set_page_config(page_title="Ladder Builder", layout="wide")
st.title("🧗 Word Ladder Interactive Builder")

@st.cache_resource
def load_engine():
    if os.path.exists('dictionary.txt'):
        with open('dictionary.txt', 'r') as f:
            words = [l.strip().lower() for l in f if l.strip()]
    else:
        words = ["head", "heal", "teal", "tell", "tall", "tail", "read", "bead", "real", "sex", "set", "sea"]
    return WordLadder(words)

engine = load_engine()

# Initialize Session State
if 'current_path' not in st.session_state:
    st.session_state.current_path = ["head"]
if 'target_word' not in st.session_state:
    st.session_state.target_word = "tail"

# Sidebar Controls
with st.sidebar:
    st.header("Configuration")
    ops = {
        'swap': st.checkbox("Swaps", True),
        'ins': st.checkbox("Insertions", True),
        'del': st.checkbox("Deletions", True)
    }
    
    new_start = st.text_input("Reset Start Word", value="head").lower()
    new_target = st.text_input("Set Target Word", value="tail").lower()
    
    if st.button("Reset Ladder"):
        st.session_state.current_path = [new_start]
        st.session_state.target_word = new_target
        st.rerun()

# Main Interface
st.subheader(f"Target: **{st.session_state.target_word.upper()}**")

# Display the Path so far
for i, step_word in enumerate(st.session_state.current_path):
    cols = st.columns([1, 4])
    
    with cols[0]:
        st.markdown(f"### `{step_word.upper()}`")
    
    with cols[1]:
        # Get neighbors for this step
        neighbors = engine.get_neighbors(step_word, ops)
        
        # Highlight the neighbor that leads to the shortest remaining path
        shortest_to_target = engine.find_shortest(step_word, st.session_state.target_word, ops)
        suggested_next = shortest_to_target[1] if shortest_to_target and len(shortest_to_target) > 1 else None

        # Create clickable buttons for neighbors
        # We only show neighbors for the LAST word in the path to keep UI clean
        if i == len(st.session_state.current_path) - 1:
            if step_word == st.session_state.target_word:
                st.balloons()
                st.success("Target Reached!")
            else:
                st.write("Choose the next step:")
                # Display buttons in a row
                btn_cols = st.columns(min(len(neighbors), 8) if neighbors else 1)
                for idx, n_word in enumerate(neighbors):
                    col_idx = idx % len(btn_cols)
                    is_suggested = (n_word == suggested_next)
                    
                    label = f"✨ {n_word}" if is_suggested else n_word
                    if btn_cols[col_idx].button(label, key=f"{step_word}_{n_word}"):
                        st.session_state.current_path.append(n_word)
                        st.rerun()
                if not neighbors:
                    st.error("Dead end! No reachable neighbors.")
        else:
            st.info(f"Step {i+1} chosen.")

if st.session_state.current_path[-1] != st.session_state.target_word:
    if st.button("Undo Last Step"):
        if len(st.session_state.current_path) > 1:
            st.session_state.current_path.pop()
            st.rerun()