# Python DP Tips (from state-frontier style)

## 1) Use tuple keys for grid states
Tuples are hashable and work well as dictionary keys for coordinates.

```python
state[(x, y)] = value
```

## 2) Use nested dicts for merged states
Store per-cell best values by a second key (for example, cost).

```python
current = {(0, 0): {0: 0}}  # (x, y) -> {cost: best_score}
```

## 3) Use setdefault to initialize nested buckets
Create a nested dictionary only when missing, then update it.

```python
bucket = next_states.setdefault((nx, ny), {})
```

Equivalent verbose form:

```python
if (nx, ny) not in next_states:
    next_states[(nx, ny)] = {}
bucket = next_states[(nx, ny)]
```

## 4) Use get(default) for safe lookup
Avoid KeyError and define a fallback in one call.

```python
old = bucket.get(new_cost, -1)
```

## 5) Keep-best update pattern
Common DP trick: keep only the best score for the same state.

```python
bucket[new_cost] = max(bucket.get(new_cost, -1), new_score)
```

## 6) Dict comprehension for clean transforms
Like list comprehensions, but building a dictionary.

```python
current = {
    cell: prune_frontier(cost_map)
    for cell, cost_map in next_states.items()
}
```

## 7) Iterate key-value pairs with items()
Cleaner and faster than looping keys then indexing.

```python
for (x, y), cost_map in current.items():
    ...
```

## 8) sorted(dict_obj) sorts by keys
Useful when pruning monotonic frontiers by increasing key.

```python
for cost in sorted(cost_to_score):
    ...
```

## 9) max(..., default=...) for empty cases
Prevents ValueError when iterable might be empty.

```python
answer = max(end_scores.values(), default=-1)
```

## 10) Optional state fetch with get
Return a default object when a state is missing.

```python
end_scores = current.get((n - 1, m - 1), {})
```

## 11) Helpful type hints for nested states
Improves readability and editor support.

```python
next_states: dict[tuple[int, int], dict[int, int]] = {}
```

## 12) Frontier pruning idea
If higher cost does not improve score, discard that state.

Example rule:
- keep a state only if its score is strictly better than all lower-cost states seen so far

This can dramatically reduce DP state size.
