# Experiment 1: Knowledge Representation — Semantic Network with Inheritance

## 1. Procedure and Result

The semantic network logic, along with its extensions, was implemented in Python using a Graph/Dictionary-based optimized approach. The network is stored as an adjacency list representation (a nested dictionary) for fast lookups.

### Code Snippet (`graph_semantic_network.py`)

```python
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
```

### Execution Output

```text
--- Experiment 1: Semantic Network (Graph Variation) ---

Inheritance chain for 'penguin': ['penguin', 'bird', 'animal']
Inheritance chain for 'ostrich': ['ostrich', 'bird', 'animal']
Inheritance chain for 'shark': ['shark', 'fish', 'animal']

Query Results:
  query_graph('shark', 'has') -> skin
  query_graph('bird', 'can') -> fly
  query_graph('penguin', 'can') -> cannot fly
  query_graph('ostrich', 'can') -> run fast
  query_graph('ostrich', 'has') -> skin
  query_graph('fish', 'can') -> unknown

--- Exercise 2 & 3: Frames & Multiple Inheritance (DFS Order) ---
  db['shark'].query('has') -> skin
  db['bird'].query('can') -> fly
  db['penguin'].query('can') -> cannot fly
  db['ostrich'].query('can') -> run fast
  db['ostrich'].query('has') -> skin
  db['fish'].query('can') -> unknown
  db['penguin'].query('can') -> cannot fly
```

## 2. Observations

- **How the query for 'penguin can' returns 'cannot fly' even though birds can fly:**
  Because the traversal goes from specific (penguin) to general (bird, then animal) and exceptions are evaluated before inherited local properties, the `'cannot': ['fly']` list on the `penguin` node intercepts the query for the `can` relation. It returns `"cannot fly"` before the system even inspects the `bird` node.

- **Why exceptions must be checked before inherited values at every level of the chain:**
  Checking exceptions first maintains the logical priority of local overriding facts. Without this mechanism, an affirmative general trait would falsely apply to a specific instance that was meant to be an exception. Thus, exceptions act as "short-circuits" to the standard inheritance path.

- **What the result tells you about default reasoning being non-monotonic:**
  Default reasoning relies on assumptions (defaults) that hold as long as no contradictory evidence is found. The fact that learning "penguins cannot fly" alters our conclusion about a specific bird demonstrates its non-monotonic nature. The body of derived truths changes or retracts as more specific premises are added to the knowledge base.

## 3. Justification for Multiple Inheritance Order

In Variation 3, a **Depth-First Search (DFS)** strategy was used for the frame system inheritance.
**Justification:** DFS is another common approach (often used in languages like older Python versions for method resolution order before C3 linearization). It searches the first parent's lineage fully before checking the second parent. This is justifiable when the order of parents in the `ako` list strictly indicates priority (i.e., the first parent is the "primary" taxonomic classification, while subsequent parents are "mixins" or secondary classifications). For example, `penguin` is primarily a `bird`, and secondarily a `swimmer`.
