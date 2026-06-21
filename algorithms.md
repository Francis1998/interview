# Algorithms & Data Structures

## Table of Contents

- [Sorting Algorithms](#sorting-algorithms)
- [Heap Sort](#heap-sort)
- [Top-K Problems](#top-k-problems)
- [Hash Tables & Collisions](#hash-tables--collisions)
- [Red-Black Trees](#red-black-trees)
- [Linked Lists](#linked-lists)
- [Balanced BST Check](#balanced-bst-check)

---

## Sorting Algorithms

### Merge Sort

**Divide and conquer:**
1. Split array in half recursively until size 1.
2. Merge sorted halves in O(n) per level.
3. Total: **O(n log n)** time, **O(n)** extra space.

Stable; predictable performance; used when stability matters or linked-list sort.

### Quick Sort

**Partition around pivot:**
1. Choose pivot (last, random, or median-of-three).
2. Partition: elements < pivot left, > pivot right.
3. Recurse on both partitions.

- **Average:** O(n log n), in-place O(log n) stack.
- **Worst:** O(n²) if pivot always min/max → mitigate with random pivot.
- **Not stable** by default.

### Complexity Summary

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Insertion sort | O(n) | O(n²) | O(n²) | O(1) | Yes |

---

## Heap Sort

Max-heap property: parent ≥ children.

```python
def heapify(arr: list[int], n: int, i: int) -> None:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heapsort(arr: list[int]) -> None:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
```

- Build heap: O(n)
- Extract-max n times: O(n log n)
- **Total: O(n log n)**, in-place

---

## Top-K Problems

Given N elements, find the K largest (or smallest).

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Sort all | O(N log N) | O(N) | Simple, wasteful if K << N |
| Min-heap of size K | O(N log K) | O(K) | **Best general approach** |
| Quickselect | O(N) avg | O(1) | In-place; worst O(N²) |
| Map-reduce + heap | O(N/P + M log K) | Distributed | P workers, M merged candidates |

### Min-Heap for Top-K Largest

Maintain heap of size K with smallest at root. For each element:
- If heap size < K: push.
- Else if element > root: pop root, push element.

### Finding Median at Scale

1. **External sort** + pick middle element.
2. **Bucket by hash range** → count elements per bucket → locate median bucket → sort only that bucket.

---

## Hash Tables & Collisions

### Collision Resolution

1. **Chaining:** Each bucket is a linked list (or tree if chain > threshold — Java HashMap → red-black tree at length 8).
2. **Open addressing:** Probe for next empty slot (linear, quadratic, double hashing).
3. **Rehashing:** When load factor exceeds threshold, grow table and rehash all entries.

**Interview follow-up:** Long chains degrade to O(n) → convert bucket to balanced BST (O(log n) per lookup in that bucket).

---

## Red-Black Trees

Self-balancing BST guaranteeing O(log n) operations.

**Properties:**
1. Every node is red or black.
2. Root is black.
3. All leaves (NIL) are black.
4. Red node → both children black.
5. Every path from node to descendant leaf has the same number of black nodes.

**Why not strict AVL?** Red-black allows slightly looser balance → fewer rotations on insert/delete → better for frequent updates.

**Uses:** `std::map`, Linux kernel rbtree, Java `TreeMap`, CFS scheduler.

---

## Linked Lists

- **Singly linked:** O(1) insert/delete at known node; O(n) search.
- **Doubly linked:** O(1) delete with node pointer; more memory.
- **vs Array:** No random access; no reallocation on insert; cache-unfriendly.

Common patterns: fast/slow pointers (cycle detection), dummy head node, reverse in-place.

---

## Balanced BST Check

Verify tree is height-balanced (|left height − right height| ≤ 1 at every node):

```python
def check_balance(root) -> int:
    if root is None:
        return 0
    left = check_balance(root.left)
    if left == -1:
        return -1
    right = check_balance(root.right)
    if right == -1:
        return -1
    if abs(left - right) > 1:
        return -1
    return max(left, right) + 1
```

Return -1 on imbalance; otherwise return subtree height.

---

## Brain Teasers (Quick Reference)

### Poisoned Wine

1000 bottles, 10 mice → binary encoding. Mouse *i* drinks bottles with bit *i* set. Dead mice = poisoned bottle index.

### Bitmap Deduplication

For integer IDs in range [0, N): use bit array — O(N/8) bytes. 2-bit variant detects duplicates in one pass.
