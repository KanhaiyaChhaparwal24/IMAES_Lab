def build_graph(triples):
    graph = {}
    for subj, rel, obj in triples:
        if subj not in graph:
            graph[subj] = {'is-a': [], 'cannot': [], 'props': {}}
        
        if rel == 'is-a':
            graph[subj]['is-a'].append(obj)
        elif rel == 'cannot':
            graph[subj]['cannot'].append(obj)
        else:
            graph[subj]['props'][rel] = obj
            
    return graph

def get_inheritance_chain_graph(node, graph):
    chain = []
    current = node
    while current:
        chain.append(current)
        parents = graph.get(current, {}).get('is-a', [])
        # Single inheritance for this part
        current = parents[0] if parents else None
    return chain

def query_graph(node, relation, graph):
    chain = get_inheritance_chain_graph(node, graph)
    for current in chain:
        node_data = graph.get(current, {})
        
        # Exceptions
        if relation == 'can' and node_data.get('cannot'):
            return f"cannot {node_data['cannot'][0]}"
            
        # Local properties
        if relation in node_data.get('props', {}):
            return node_data['props'][relation]
            
    return 'unknown'


class FrameDict(dict):
    """A dictionary subclass that implements inheritance via 'ako' slot."""
    def __init__(self, frames_db, name, **kwargs):
        super().__init__(**kwargs)
        self.frames_db = frames_db
        self.name = name
        
    def query(self, slot):
        # Multiple inheritance using DFS (Depth-First Search) but keeping track of visited
        # We'll use DFS for Variation 3 to show a different traversal order and justify it.
        stack = [self.name]
        visited = set()
        
        while stack:
            current_name = stack.pop()
            if current_name in visited: continue
            visited.add(current_name)
            
            if current_name not in self.frames_db:
                continue
                
            frame = self.frames_db[current_name]
            
            # Exceptions
            if slot == 'can' and 'cannot' in frame:
                return f"cannot {frame['cannot']}"
                
            # Local
            if slot in frame:
                return frame[slot]
                
            # Parents
            parents = frame.get('ako', [])
            if isinstance(parents, list):
                # Reverse to process left-to-right in standard DFS
                stack.extend(reversed(parents))
            elif parents:
                stack.append(parents)
                
        return 'unknown'


def main():
    print("--- Experiment 1: Semantic Network (Graph Variation) ---")
    
    triples = [
        ('animal', 'has', 'skin'),
        ('fish', 'is-a', 'animal'),
        ('shark', 'is-a', 'fish'),
        ('bird', 'is-a', 'animal'),
        ('bird', 'can', 'fly'),
        ('penguin', 'is-a', 'bird'),
        ('penguin', 'cannot', 'fly'),
        ('ostrich', 'is-a', 'bird'),
        ('ostrich', 'cannot', 'fly'),
        ('ostrich', 'can', 'run fast')
    ]
    
    graph = build_graph(triples)

    print("\nInheritance chain for 'penguin':", get_inheritance_chain_graph('penguin', graph))
    print("Inheritance chain for 'ostrich':", get_inheritance_chain_graph('ostrich', graph))
    print("Inheritance chain for 'shark':", get_inheritance_chain_graph('shark', graph))

    queries = [
        ('shark', 'has'),
        ('bird', 'can'),
        ('penguin', 'can'),
        ('ostrich', 'can'),
        ('ostrich', 'has'),
        ('fish', 'can')
    ]
    
    print("\nQuery Results:")
    for q_node, q_rel in queries:
        print(f"  query_graph('{q_node}', '{q_rel}') -> {query_graph(q_node, q_rel, graph)}")


    print("\n--- Exercise 2 & 3: Frames & Multiple Inheritance (DFS Order) ---")
    db = {}
    db['animal'] = FrameDict(db, 'animal', has='skin')
    db['bird'] = FrameDict(db, 'bird', ako=['animal'], can='fly')
    db['fish'] = FrameDict(db, 'fish', ako=['animal'])
    db['shark'] = FrameDict(db, 'shark', ako=['fish'])
    db['swimmer'] = FrameDict(db, 'swimmer', can='swim')
    db['penguin'] = FrameDict(db, 'penguin', ako=['bird', 'swimmer'], cannot='fly')
    db['ostrich'] = FrameDict(db, 'ostrich', ako=['bird'], cannot='fly', can='run fast')

    for q_node, q_rel in queries:
        print(f"  db['{q_node}'].query('{q_rel}') -> {db[q_node].query(q_rel)}")

    print(f"  db['penguin'].query('can') -> {db['penguin'].query('can')}")


if __name__ == "__main__":
    main()
