# Unit 4 — Advanced Data Structures

## Short Questions (2 Marks)

### Question 1
**Question**  
Define a comprehension in Python.

**Answer**  
A comprehension is a compact, single-line construct for building a new collection by transforming and/or filtering an existing iterable.

**Topic**  
Comprehensions

---

### Question 2
**Question**  
State the syntax of a list comprehension.

**Answer**  
The syntax is: `[expression for item in iterable if condition]`.

**Topic**  
List Comprehensions

---

### Question 3
**Question**  
Differentiate between the two positions of `if` in a comprehension.

**Answer**  
When `if` is placed at the end, it acts as a filter and removes non-matching items. When `if/else` is placed in the expression, it transforms every item and keeps all of them.

**Topic**  
Comprehension Filters and Transformations

---

### Question 4
**Question**  
State one common use of nested list comprehensions.

**Answer**  
Nested list comprehensions are used for flattening a 2-D list or building a 2-D structure such as a table.

**Topic**  
Nested List Comprehensions

---

### Question 5
**Question**  
Define a dictionary comprehension.

**Answer**  
A dictionary comprehension builds a new dictionary directly from an iterable using the form `{key_expression: value_expression for item in iterable if condition}`.

**Topic**  
Dictionary Comprehensions

---

### Question 6
**Question**  
What is a set comprehension?

**Answer**  
A set comprehension uses `{}` without a colon and creates a set, removing duplicates automatically.

**Topic**  
Set Comprehensions

---

### Question 7
**Question**  
Define a default parameter.

**Answer**  
A default parameter is a parameter that has a pre-assigned value and is used when the caller does not provide an argument for it.

**Topic**  
Default Parameters

---

### Question 8
**Question**  
What is the mutable default argument trap?

**Answer**  
It occurs when a mutable object such as a list or dictionary is used as a default parameter, because that object is created once at function definition time and shared across calls.

**Topic**  
Mutable Default Trap

---

### Question 9
**Question**  
What does `*args` receive in a function?

**Answer**  
`*args` receives a tuple of extra positional arguments.

**Topic**  
`*args`

---

### Question 10
**Question**  
What does `**kwargs` receive in a function?

**Answer**  
`**kwargs` receives a dictionary of extra keyword arguments.

**Topic**  
`**kwargs`

---

### Question 11
**Question**  
What is the purpose of the `key` parameter in `sorted()` and `list.sort()`?

**Answer**  
The `key` parameter tells Python to apply a function to each item before comparing items for sorting.

**Topic**  
Specialized Sorting

---

### Question 12
**Question**  
How is `lambda` used in sorting?

**Answer**  
A `lambda` is used as a short one-expression key function when sorting complex objects or dictionaries.

**Topic**  
`lambda` and Sorting

---

### Question 13
**Question**  
List any two operations supported by `deque`.

**Answer**  
Examples are `append()`, `appendleft()`, `pop()`, and `popleft()`.

**Topic**  
`deque`

---

### Question 14
**Question**  
Why is `deque` preferred over `list` for left-side operations?

**Answer**  
`deque` supports O(1) operations at both ends, whereas `list` performs left-side operations in O(n) time.

**Topic**  
`deque` Performance

---

### Question 15
**Question**  
Define a `namedtuple`.

**Answer**  
A `namedtuple` is a tuple with named fields, making data more readable while still remaining immutable.

**Topic**  
`namedtuple`

---

### Question 16
**Question**  
What does `._asdict()` do for a `namedtuple`?

**Answer**  
`._asdict()` converts the namedtuple into a dictionary.

**Topic**  
`namedtuple` Conversion

---

### Question 17
**Question**  
How does a `ChainMap` search for keys?

**Answer**  
A `ChainMap` searches the dictionaries from left to right, and the first matching key wins.

**Topic**  
`ChainMap`

---

### Question 18
**Question**  
What happens when a missing key is accessed in a `Counter`?

**Answer**  
A missing key returns `0` and does not raise `KeyError`.

**Topic**  
`Counter`

---

### Question 19
**Question**  
State one unique feature of `OrderedDict`.

**Answer**  
`OrderedDict` supports `move_to_end()` and also treats dictionaries with the same items but different order as unequal.

**Topic**  
`OrderedDict`

---

### Question 20
**Question**  
What does `defaultdict` do when a key does not exist?

**Answer**  
`defaultdict` auto-creates the missing key using the specified default factory, such as `list`, `int`, or `set`.

**Topic**  
`defaultdict`

---

## Medium Questions (5 Marks)

### Question 1
**Question**  
Explain list comprehensions and give one example from the notes.

**Answer**  
A list comprehension is a compact way to create a list by transforming or filtering an iterable. It uses the form `[expression for item in iterable if condition]`. For example, `[score for score in scores if score >= 50]` creates a list of passing scores.

**Topic**  
List Comprehensions

---

### Question 2
**Question**  
Explain nested list comprehensions with reference to flattening and building 2-D structures.

**Answer**  
Nested list comprehensions contain two `for` clauses and mirror nested loops. They are useful for flattening a 2-D list into one list and for building a 2-D structure such as a multiplication table or a grid of values.

**Topic**  
Nested List Comprehensions

---

### Question 3
**Question**  
Describe dictionary comprehensions and explain one example of filtering and one example of transformation.

**Answer**  
Dictionary comprehensions build a dictionary directly from an iterable. They may be used to filter items, such as keeping only passing students, or to transform values, such as converting scores to letter grades.

**Topic**  
Dictionary Comprehensions

---

### Question 4
**Question**  
Explain default parameters and the mutable default argument trap. Also state the safe fix.

**Answer**  
Default parameters are assigned values that are used when no argument is supplied. However, if the default is a mutable object such as a list, it is created once and shared by all calls. The safe fix is to use `None` as a sentinel and create the object inside the function.

**Topic**  
Default Parameters and Mutable Defaults

---

### Question 5
**Question**  
Explain the use of `*args` and `**kwargs` in Python functions.

**Answer**  
`*args` collects extra positional arguments as a tuple, while `**kwargs` collects extra keyword arguments as a dictionary. They are useful for writing flexible functions that accept any number of arguments. They can also be used at the call site with `*` and `**` for unpacking.

**Topic**  
Variable Arguments

---

### Question 6
**Question**  
Discuss sorting with `sorted()`, `key`, `lambda`, and `itemgetter`.

**Answer**  
The `key` parameter allows sorting to be based on a function applied to each item before comparison. A `lambda` can be used for short one-expression key functions, while `itemgetter` from the `operator` module is more readable for sorting dictionaries by specific keys.

**Topic**  
Specialized Sorting

---

### Question 7
**Question**  
Describe `namedtuple` and explain its advantages.

**Answer**  
A `namedtuple` is a lightweight immutable record with named fields. It allows access by field name, is still tuple-like, and can be converted to a dictionary using `._asdict()`. It is more readable than using plain indexes and lighter than creating a full class.

**Topic**  
`namedtuple`

---

### Question 8
**Question**  
Explain `deque` and compare it with `list`.

**Answer**  
A `deque` is a double-ended queue that supports fast operations at both ends. It is useful for appending and popping from the left or right, whereas a list is slower for left-side operations. `deque` also supports features like `maxlen` and `rotate()`.

**Topic**  
`deque`

---

### Question 9
**Question**  
Explain how `ChainMap` works and how it is used.

**Answer**  
A `ChainMap` combines multiple dictionaries into one searchable view without copying data. Keys are searched from left to right, and the first match is used. Updates go to the first dictionary, while other dictionaries can be changed through `.maps` or `new_child()`.

**Topic**  
`ChainMap`

---

### Question 10
**Question**  
Explain the `Counter` container and its uses.

**Answer**  
A `Counter` is a dictionary subclass used for counting hashable objects. It can count items from a list, count words in a sentence, and support arithmetic operations such as addition and subtraction. Missing keys return `0` instead of raising `KeyError`.

**Topic**  
`Counter`

---

### Question 11
**Question**  
Differentiate between `OrderedDict` and `defaultdict`.

**Answer**  
`OrderedDict` is order-aware and supports operations such as `move_to_end()`, while `defaultdict` automatically creates missing keys using a specified factory. `OrderedDict` is mainly concerned with order and order-sensitive equality, whereas `defaultdict` is used for grouping and counting.

**Topic**  
`OrderedDict` and `defaultdict`

---

### Question 12
**Question**  
Explain the purpose of `UserDict`, `UserList`, and `UserString`.

**Answer**  
These classes act as wrappers around the built-in containers and are used when a custom container is needed with extra validation or modified behavior. They are useful because they make it safer to subclass built-in containers than subclassing the built-in types directly.

**Topic**  
Wrapper Classes in `collections`

---

## Long Questions (10 Marks)

### Question 1
**Question**  
Discuss comprehensions in Python, including list comprehensions, nested list comprehensions, and dictionary comprehensions.

**Answer**  
Comprehensions are compact constructs for building new collections from existing iterables. A list comprehension uses the form `[expression for item in iterable if condition]` and can be used to filter and transform values. Nested list comprehensions contain two `for` clauses and are useful for flattening a 2-D list or creating 2-D structures. Dictionary comprehensions build dictionaries directly from iterables and can also be used for filtering or transforming data. The notes also mention set comprehensions and generator expressions as related forms.

**Topic**  
Comprehensions

---

### Question 2
**Question**  
Discuss default parameters in Python and explain the mutable default argument trap with the correct approach to avoid it.

**Answer**  
Default parameters allow a function to use a pre-assigned value when the caller does not supply one. Parameters with defaults must appear after the required parameters. A common error is using a mutable object as a default value because it is created only once at function definition time and then shared by all calls. The safe approach is to use `None` as the default and create a new object inside the function. This ensures that each call works independently.

**Topic**  
Default Parameters and Safe Function Design

---

### Question 3
**Question**  
Discuss `*args` and `**kwargs` in Python and explain how they are used in functions and call sites.

**Answer**  
`*args` accepts any number of positional arguments and receives them as a tuple. `**kwargs` accepts any number of keyword arguments and receives them as a dictionary. They allow functions to be more flexible and reusable. The notes also show that `*` and `**` can be used at the call site to unpack a list or dictionary into positional or keyword arguments. This makes it easier to pass collected data into functions.

**Topic**  
Variable Arguments and Unpacking

---

### Question 4
**Question**  
Evaluate the importance of sorting with `key`, `lambda`, and `itemgetter` in Python.

**Answer**  
Sorting with `key` is important because it allows items to be compared according to a transformed value instead of the original object. For example, `sorted(names, key=len)` sorts by length. A `lambda` is useful for short one-expression functions, especially when sorting a list of dictionaries by a specific key. `itemgetter` from the `operator` module is presented as a more readable alternative when sorting by dictionary keys. The notes also show that tuples can be sorted left to right, which is useful for multi-level order.

**Topic**  
Specialized Sorting

---

### Question 5
**Question**  
Describe the `collections` module with emphasis on `namedtuple` and `deque`.

**Answer**  
The `collections` module provides specialized container types beyond the built-in containers. A `namedtuple` is a tuple with named fields and combines readability with immutability. It allows field access by name and can be converted to a dictionary using `._asdict()`. A `deque` is a double-ended queue that supports efficient operations at both ends and is useful for queues, sliding windows, and rotating elements. The notes also explain that `deque` is more efficient than `list` for left operations.

**Topic**  
`namedtuple` and `deque`

---

### Question 6
**Question**  
Discuss `ChainMap` and `Counter` as specialized containers in the `collections` module.

**Answer**  
A `ChainMap` groups multiple dictionaries into one searchable view without copying data. It searches left to right, and the first matching key is used. Updates go to the first dictionary, while other layers can be changed through `.maps` or `new_child()`. A `Counter` is a dictionary subclass used for counting hashable objects. It returns `0` for missing keys instead of raising `KeyError`, and it supports operations such as counting words and combining counts through arithmetic.

**Topic**  
`ChainMap` and `Counter`

---

### Question 7
**Question**  
Explain `OrderedDict` and `defaultdict` and discuss their uses in Python.

**Answer**  
`OrderedDict` preserves insertion order and offers features such as `move_to_end()`. It is also order-sensitive in equality comparisons, which means that two ordered dictionaries with the same items but a different order are not considered equal. `defaultdict` is a dictionary subclass that auto-creates missing keys using a default factory such as `list`, `int`, or `set`. It is especially useful for grouping items and counting values without repeatedly checking key existence.

**Topic**  
`OrderedDict` and `defaultdict`

---

### Question 8
**Question**  
Discuss `UserDict`, `UserList`, and `UserString` and explain why they are used in Python programs.

**Answer**  
`UserDict`, `UserList`, and `UserString` are wrapper classes in the `collections` module. They are used when developers want to create custom containers with modified or additional behavior. The notes explain that they are safer than subclassing the built-in container types directly because methods such as `update()` may bypass custom logic. These wrappers allow validation, controlled deletion, and custom string operations, making them suitable for building reliable custom containers.

**Topic**  
Wrapper Classes in `collections`