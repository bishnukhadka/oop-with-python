# Part B - Threads

**Course:** BT151CO - Object-Oriented Programming  

| | |
|---|---|
| **Duration** | 6 Hours |
| **CLO** | CLO 6 - Apply advanced Python modules to solve real-world text processing and concurrency problems |
| **Pre-requisite** | Unit 7 - Network Programming; Unit 2 - OOP |
---

## Table of Contents

**Part B : Threads**

11. [Processes and Threads](#11-processes-and-threads)
12. [Multi-threading in Python](#12-multi-threading-in-python)
13. [Synchronization](#13-synchronization)
14. [Thread Life Cycle](#14-thread-life-cycle)

# 11. Processes and Threads


## 11.1 The Problem - Doing Multiple Things at Once

Imagine a **bank branch**. When you walk in, a single cashier serves you while everyone else waits in a queue. This is **sequential processing** - one task at a time. As the queue grows, customers wait longer and longer.

Now the bank hires **five cashiers**. Each customer is served simultaneously. This is **concurrent processing** - multiple tasks at the same time.

Your Python programs face the same problem. When a program downloads a file, should everything else freeze while it waits? When a game runs, should the screen stop updating while the physics engine calculates? The answer is no - and threads solve this.

---

## 11.2 What Is a Process?

A **process** is a running instance of a program. When you double-click Python's interpreter, your operating system creates a process:

- It gets its **own block of memory** (private - nothing else can read it)
- It has its **own CPU time**
- It has its **own file handles**, network connections, etc.

When you open two Python scripts at the same time, you have **two separate processes**. They cannot share variables - they are completely isolated.

| Property | Process |
|---|---|
| Memory | **Private** - each process has its own |
| Communication | Slow - must use files, sockets, or pipes |
| Crash isolation | A crash in one process does NOT affect others |
| Startup cost | **High** - the OS does a lot of work |

---

## 11.3 What Is a Thread?

A **thread** is a unit of execution **within** a process. A single process can contain many threads. All threads in a process **share the same memory**.

Think of a process as a **library building** and threads as **librarians** working inside it:
- All librarians share the same shelves (memory)
- They can all read and modify the same books (variables)
- They work simultaneously on different tasks
- If one librarian drops a book in the wrong place, other librarians might be confused - this is the **concurrency problem**

| Property | Thread |
|---|---|
| Memory | **Shared** - all threads in a process see the same variables |
| Communication | **Fast** - just read and write shared variables |
| Crash isolation | A crash in one thread can crash the whole process |
| Startup cost | **Low** - much cheaper than a new process |

---

## 11.4 Process vs Thread - Side by Side

| Feature | Process | Thread |
|---|---|---|
| Memory | Separate | Shared |
| Communication | Slow (IPC) | Fast (shared variables) |
| Creation cost | High | Low |
| Crash isolation | Good | Poor |
| Use case | CPU-heavy tasks | I/O-heavy tasks |
| Python module | `multiprocessing` | `threading` |

---

## 11.5 The GIL - Python's Global Interpreter Lock

Python has a mechanism called the **Global Interpreter Lock (GIL)**. You do not need to understand the internals, but you need to know its effect:

> **The GIL ensures that only ONE thread executes Python bytecode at a time**, even on a multi-core processor.

This means Python threads do **not** speed up CPU-bound tasks (like heavy calculations). They **do** help with **I/O-bound tasks** - tasks that spend most of their time waiting (downloading files, reading from disk, waiting for database queries, waiting for user input).

| Task type | Example | Use threads? |
|---|---|---|
| I/O-bound | Downloading 5 files | Yes - threads help |
| CPU-bound | Calculating primes | No - use `multiprocessing` |

For this unit, we focus on **threading** for I/O-bound work, which is the most common use case in web apps and everyday programs.

---

# 12. Multi-threading in Python

## 12.1 The `threading` Module

Python's `threading` module provides the `Thread` class for creating and managing threads.

```python
import threading
```

**The key class:**

```python
threading.Thread(
    target=function_name,  # the function the thread will run
    args=(arg1, arg2),     # arguments to pass (must be a tuple)
    name="MyThread",       # optional - human-readable name
    daemon=False           # whether to auto-exit when main thread ends
)
```

---

## 12.2 Creating and Starting a Thread - Minimal Example

```python
import threading
import time

def say_hello(name):
    """A simple function that will run in its own thread."""
    print(f"[Thread] Hello from {name}!")
    time.sleep(1)   # simulate some work
    print(f"[Thread] {name} is done.")

# Step 1: Create the Thread object (does NOT start yet)
t = threading.Thread(target=say_hello, args=("Alice",))

# Step 2: Start the thread (NOW it begins running)
t.start()

print("[Main] Thread has been started.")

# Step 3: Wait for the thread to finish before continuing
t.join()

print("[Main] Thread has finished. Program ends.")
```

```
[Main] Thread has been started.
[Thread] Hello from Alice!
[Thread] Alice is done.
[Main] Thread has finished. Program ends.
```

> Note: `[Main] Thread has been started.` may print before or after the thread's first print - the order depends on the operating system's scheduler. This non-determinism is fundamental to concurrent programs.

---

## 12.3 Running Multiple Threads - Library Book Processing

```python
import threading
import time

def process_book_order(student_name, book_title, processing_time):
    """Simulate processing a library book order."""
    print(f"  Processing '{book_title}' for {student_name}...")
    time.sleep(processing_time)  # simulate network/disk I/O
    print(f"  Done: '{book_title}' is ready for {student_name}.")

# Without threads (sequential) - total time = sum of all times
print("=== Sequential (without threads) ===")
start = time.time()
process_book_order("Alice", "Fluent Python", 2)
process_book_order("Bob",   "Clean Code",    1)
process_book_order("Diana", "Python Cookbook", 1.5)
print(f"Sequential time: {time.time() - start:.1f}s\n")

# With threads (concurrent) - total time ≈ longest single task
print("=== Concurrent (with threads) ===")
orders = [
    ("Alice", "Fluent Python",   2),
    ("Bob",   "Clean Code",      1),
    ("Diana", "Python Cookbook", 1.5),
]

threads = []
start = time.time()

for student, book, duration in orders:
    t = threading.Thread(target=process_book_order, args=(student, book, duration))
    threads.append(t)
    t.start()

# Wait for ALL threads to complete
for t in threads:
    t.join()

print(f"Concurrent time: {time.time() - start:.1f}s")
```

```
=== Sequential (without threads) ===
  Processing 'Fluent Python' for Alice...
  Done: 'Fluent Python' is ready for Alice.
  Processing 'Clean Code' for Bob...
  Done: 'Clean Code' is ready for Bob.
  Processing 'Python Cookbook' for Diana...
  Done: 'Python Cookbook' is ready for Diana.
Sequential time: 4.5s

=== Concurrent (with threads) ===
  Processing 'Fluent Python' for Alice...
  Processing 'Clean Code' for Bob...
  Processing 'Python Cookbook' for Diana...
  Done: 'Clean Code' is ready for Bob.
  Done: 'Python Cookbook' is ready for Diana.
  Done: 'Fluent Python' is ready for Alice.
Concurrent time: 2.0s
```

Sequential takes 4.5 seconds (2 + 1 + 1.5). Concurrent takes only 2 seconds (the longest single task) - a 55% improvement.

---

## 12.4 Daemon Threads

A **daemon thread** runs in the background and is automatically killed when the main program finishes - even if the thread has not completed its work. Use `daemon=True` for background tasks that should not prevent the program from exiting.

```python
import threading
import time

def background_autosave():
    """Periodically save game progress in the background."""
    count = 0
    while True:
        count += 1
        time.sleep(2)
        print(f"  [AutoSave] Game progress saved (save #{count})")

# daemon=True: this thread will be killed when the main thread ends
save_thread = threading.Thread(target=background_autosave, daemon=True)
save_thread.start()

print("[Game] Game started.")
time.sleep(5)   # simulate 5 seconds of gameplay
print("[Game] Game over.")
# The autosave daemon thread is automatically killed here
```

```
[Game] Game started.
  [AutoSave] Game progress saved (save #1)
  [AutoSave] Game progress saved (save #2)
[Game] Game over.
```

> **Rule:** Use `daemon=True` for background helper threads (logging, auto-save, heartbeats). Use `daemon=False` (the default) for threads that must finish their work before the program exits.

---

## 12.5 Subclassing `Thread` - The OOP Approach

You can create a thread by subclassing `threading.Thread` and overriding `run()`. This is useful for more complex threads that need state.

```python
import threading
import time

class StudentWorker(threading.Thread):
    """A thread that represents a student completing an assignment."""

    def __init__(self, name, subject, time_needed):
        super().__init__()   # MUST call Thread.__init__()
        self.student_name = name
        self.subject      = subject
        self.time_needed  = time_needed
        self.result       = None   # will be set when done

    def run(self):
        """This method runs in the new thread when .start() is called."""
        print(f"  {self.student_name} started working on {self.subject}...")
        time.sleep(self.time_needed)
        self.result = f"{self.student_name}'s {self.subject} assignment: Grade A"
        print(f"  {self.student_name} finished {self.subject}!")

# Create student worker threads
workers = [
    StudentWorker("Alice",   "Maths",   1.5),
    StudentWorker("Bob",     "English", 1.0),
    StudentWorker("Charlie", "Science", 2.0),
]

print("Assignment session begins:")
for w in workers:
    w.start()

for w in workers:
    w.join()

print("\nResults:")
for w in workers:
    print(f"  {w.result}")
```

```
Assignment session begins:
  Alice started working on Maths...
  Bob started working on English...
  Charlie started working on Science...
  Bob finished English!
  Alice finished Maths!
  Charlie finished Science!

Results:
  Alice's Maths assignment: Grade A
  Bob's English assignment: Grade A
  Charlie's Science assignment: Grade A
```

---

# 13. Synchronization

---

## 13.1 The Race Condition Problem

When multiple threads share data and modify it simultaneously, something called a **race condition** can occur. The outcome depends on which thread runs first - and that is unpredictable.

**Real-world analogy - the bank account problem:**

Imagine two bank clerks (threads) both reading the same balance at the same moment:

```
Balance: £1000

Clerk A reads:  £1000      Clerk B reads:  £1000
Clerk A adds £200          Clerk B adds £300
Clerk A writes: £1200      Clerk B writes: £1300

Final balance: £1300   ← WRONG! Should be £1500
```

One of the updates was **lost** because both threads read the old value before either wrote the new one.

---

## 13.2 Demonstrating the Race Condition

```python
import threading

# Shared bank account balance
balance = 0

def deposit(amount, count):
    """Deposit 'amount', repeated 'count' times - UNSAFE version."""
    global balance
    for _ in range(count):
        current = balance
        # Simulate the delay between reading and writing
        balance = current + amount

# Start two threads both depositing simultaneously
t1 = threading.Thread(target=deposit, args=(1, 100_000))
t2 = threading.Thread(target=deposit, args=(1, 100_000))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Expected balance: 200000")
print(f"Actual balance  : {balance}")
print(f"Difference      : {200_000 - balance} (lost updates!)")
```

```
Expected balance: 200000
Actual balance  : 183421
Difference      : 16579 (lost updates!)
```

> The exact number varies each run. This non-determinism is the hallmark of a race condition.

---

## 13.3 The Solution - `threading.Lock`

A **lock** (also called a **mutex** - mutual exclusion object) ensures that only **one thread** can execute a critical section of code at a time. All other threads must **wait**.

```python
import threading

balance = 0
lock = threading.Lock()   # Create the lock

def safe_deposit(amount, count):
    """Deposit 'amount', repeated 'count' times - SAFE version."""
    global balance
    for _ in range(count):
        with lock:          # Acquire the lock (other threads wait here)
            current = balance
            balance = current + amount
            # Lock is released automatically when 'with' block ends

t1 = threading.Thread(target=safe_deposit, args=(1, 100_000))
t2 = threading.Thread(target=safe_deposit, args=(1, 100_000))

t1.start()
t2.start()
t1.join()
t2.join()

print(f"Expected balance: 200000")
print(f"Actual balance  : {balance}")
print(f"Correct         : {balance == 200_000}")
```

```
Expected balance: 200000
Actual balance  : 200000
Correct         : True
```

---

## 13.4 How `Lock` Works - Step by Step

```
Thread 1                         Thread 2
─────────────────────────────    ─────────────────────────────
lock.acquire()  ← succeeds       lock.acquire()  ← BLOCKS (waits)
  reads balance                  
  writes balance                 
lock.release()                   
                                 lock.acquire()  ← now succeeds
                                   reads balance
                                   writes balance
                                 lock.release()
```

The `with lock:` pattern is equivalent to:

```python
lock.acquire()
try:
    # critical section
finally:
    lock.release()   # always released, even if an exception occurs
```

Always use `with lock:` - it is safer because it guarantees the lock is released.

---

## 13.5 Example - Thread-Safe Library Book Checkout

```python
import threading

class Library:
    """A thread-safe library with a limited number of copies per book."""

    def __init__(self):
        self._inventory = {
            "Fluent Python":   3,
            "Clean Code":      2,
            "Python Cookbook": 1,
        }
        self._lock = threading.Lock()

    def checkout(self, student_name, book_title):
        """Check out one copy of a book - thread-safe."""
        with self._lock:
            copies = self._inventory.get(book_title, 0)
            if copies > 0:
                self._inventory[book_title] -= 1
                print(f"  OK:  {student_name} checked out '{book_title}' "
                      f"({copies - 1} copies left)")
                return True
            else:
                print(f"  FAIL: No copies of '{book_title}' available for {student_name}")
                return False

library = Library()

# Multiple students trying to check out books simultaneously
checkouts = [
    ("Alice",   "Python Cookbook"),
    ("Bob",     "Python Cookbook"),   # only 1 copy - Bob should fail
    ("Charlie", "Clean Code"),
    ("Diana",   "Clean Code"),
    ("Eve",     "Fluent Python"),
]

threads = [
    threading.Thread(target=library.checkout, args=(s, b))
    for s, b in checkouts
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

```
  OK:  Alice checked out 'Python Cookbook' (0 copies left)
  FAIL: No copies of 'Python Cookbook' available for Bob
  OK:  Charlie checked out 'Clean Code' (1 copies left)
  OK:  Diana checked out 'Clean Code' (0 copies left)
  OK:  Eve checked out 'Fluent Python' (2 copies left)
```

---

## 13.6 `threading.Semaphore` - Limiting Concurrent Access

A **semaphore** is a lock that allows up to N threads simultaneously (a regular lock allows only 1). Useful for limiting concurrent connections to a database or API.

```python
import threading
import time

# Only 2 students can use the computer lab at once
lab_semaphore = threading.Semaphore(2)

def use_computer_lab(student_name):
    """Student enters the lab, uses a computer, then leaves."""
    print(f"  {student_name} is waiting to enter the lab...")
    with lab_semaphore:          # Blocks if 2 others are already inside
        print(f"  {student_name} entered the lab.")
        time.sleep(1.5)          # simulate using the computer
        print(f"  {student_name} has left the lab.")

students = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
threads  = [threading.Thread(target=use_computer_lab, args=(s,)) for s in students]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

```
  Alice is waiting to enter the lab...
  Alice entered the lab.
  Bob is waiting to enter the lab...
  Bob entered the lab.
  Charlie is waiting to enter the lab...
  Diana is waiting to enter the lab...
  Eve is waiting to enter the lab...
  Alice has left the lab.
  Charlie entered the lab.
  Bob has left the lab.
  Diana entered the lab.
  Charlie has left the lab.
  Eve entered the lab.
  Diana has left the lab.
  Eve has left the lab.
```

> Notice that Charlie, Diana, and Eve all wait while Alice and Bob are inside. The semaphore enforces the limit of 2.

---

## 13.7 `threading.Event` - Signalling Between Threads

An **Event** lets one thread signal another to start, stop, or change what it is doing.

```python
import threading
import time

# Game scenario: a "game over" event stops background threads
game_over = threading.Event()

def score_tracker():
    """Keep incrementing the score until the game ends."""
    score = 0
    while not game_over.is_set():
        score += 10
        time.sleep(0.5)
    print(f"  [ScoreTracker] Final score: {score}")

def enemy_spawner():
    """Keep spawning enemies until the game ends."""
    count = 0
    while not game_over.is_set():
        count += 1
        print(f"  [EnemySpawner] Enemy #{count} spawned!")
        time.sleep(1)
    print(f"  [EnemySpawner] Stopped. Total enemies: {count}")

# Start background threads
t1 = threading.Thread(target=score_tracker, daemon=True)
t2 = threading.Thread(target=enemy_spawner, daemon=True)
t1.start()
t2.start()

# Main game loop: runs for 3 seconds
time.sleep(3)
print("\n[Main] Game over! Signalling threads to stop...")
game_over.set()   # Signal the event - threads will see is_set() = True

t1.join()
t2.join()
print("[Main] All threads stopped.")
```

```
  [EnemySpawner] Enemy #1 spawned!
  [EnemySpawner] Enemy #2 spawned!
  [EnemySpawner] Enemy #3 spawned!

[Main] Game over! Signalling threads to stop...
  [ScoreTracker] Final score: 60
  [EnemySpawner] Stopped. Total enemies: 3
[Main] All threads stopped.
```

---

> **Common Mistake 3:** Not joining threads before the program ends.
>
> ```python
> t = threading.Thread(target=do_work)
> t.start()
> # BAD - program exits immediately, possibly before thread finishes
>
> t.start()
> t.join()  # GOOD - waits for thread to complete
> ```

---

# 14. Thread Life Cycle

---

## 14.1 The Five States of a Thread

A thread moves through a defined life cycle from creation to termination:

```
      ┌───────────┐
      │  NEW      │  ← Thread object created (Thread(...))
      └─────┬─────┘
            │ .start()
      ┌─────▼─────┐
      │  RUNNABLE │  ← Ready to run; waiting for CPU time
      └─────┬─────┘
            │ CPU granted
      ┌─────▼─────┐       ┌──────────────┐
      │  RUNNING  │──────▶│  BLOCKED /   │
      │           │◀──────│  WAITING     │
      └─────┬─────┘       └──────────────┘
            │ run() returns
      ┌─────▼─────┐
      │ TERMINATED│  ← Thread is done; cannot be restarted
      └───────────┘
```

| State | Description | Triggered By |
|---|---|---|
| **New** | Thread created but not started | `t = Thread(...)` |
| **Runnable** | Ready to run; waiting for CPU | `t.start()` |
| **Running** | `run()` method is executing | OS scheduler grants CPU time |
| **Blocked / Waiting** | Paused - waiting for lock, I/O, or sleep | `lock.acquire()`, `t.join()`, `time.sleep()` |
| **Terminated** | `run()` has returned or raised an unhandled exception | `run()` completes |

---

## 14.2 Demonstrating the Life Cycle

```python
import threading
import time

def lifecycle_demo():
    """Shows what each state looks like."""
    print(f"  [Thread] RUNNING - thread is executing")
    time.sleep(1)   # transitions to BLOCKED (sleeping)
    print(f"  [Thread] RUNNING again - sleep is over")
    print(f"  [Thread] About to TERMINATE...")
    # function returns → TERMINATED

print("Creating thread...")          # NEW state
t = threading.Thread(target=lifecycle_demo, name="DemoThread")
print(f"  Thread alive? {t.is_alive()}")     # False - not started yet

print("Starting thread...")          # Transitions to RUNNABLE
t.start()
print(f"  Thread alive? {t.is_alive()}")     # True - RUNNING or RUNNABLE

print("Main thread waiting (join)...")  # Main thread BLOCKED
t.join()

print(f"  Thread alive? {t.is_alive()}")     # False - TERMINATED
print("Thread has terminated.")
```

```
Creating thread...
  Thread alive? False
Starting thread...
  Thread alive? True
Main thread waiting (join)...
  [Thread] RUNNING - thread is executing
  [Thread] RUNNING again - sleep is over
  [Thread] About to TERMINATE...
  Thread alive? False
Thread has terminated.
```

---

## 14.3 Checking Active Threads

```python
import threading
import time

def worker(name, duration):
    time.sleep(duration)

threads = []
for i, (n, d) in enumerate([("Alpha", 2), ("Beta", 1), ("Gamma", 3)]):
    t = threading.Thread(target=worker, args=(n, d), name=n)
    threads.append(t)
    t.start()

time.sleep(0.1)
print("Active threads:")
for t in threading.enumerate():
    print(f"  {t.name:<15} alive={t.is_alive()}")
```

```
Active threads:
  MainThread      alive=True
  Alpha           alive=True
  Beta            alive=True
  Gamma           alive=True
```

> `threading.enumerate()` returns a list of all currently alive Thread objects, including the main thread.

---

## 14.4 Thread Exceptions - Don't Let Them Disappear Silently

If an unhandled exception occurs inside a thread's `run()` method, the thread **terminates silently** - the main thread does not know. Always wrap thread functions in `try / except`:

```python
import threading

def risky_task(student_name, score_text):
    """Process a student score - might receive invalid input."""
    try:
        score = int(score_text)      # may raise ValueError
        print(f"  {student_name}: score = {score}, grade = {'A' if score >= 90 else 'B'}")
    except ValueError as e:
        print(f"  ERROR for {student_name}: invalid score '{score_text}' - {e}")

student_data = [
    ("Alice",   "95"),
    ("Bob",     "not_a_number"),    # will cause ValueError
    ("Charlie", "82"),
]

threads = [
    threading.Thread(target=risky_task, args=(name, score))
    for name, score in student_data
]

for t in threads:
    t.start()
for t in threads:
    t.join()
```

```
  Alice: score = 95, grade = A
  ERROR for Bob: invalid score 'not_a_number' - invalid literal for int() with base 10: 'not_a_number'
  Charlie: score = 82, grade = B
```

---

---

# Part C - Framework Overview

---

# 15. Django Framework Overview

---

## 15.1 What Is Django?

**Django** is a high-level Python web framework that lets you build fully featured websites and web applications rapidly. It was created in 2003 and is used by some of the most visited websites in the world - Instagram, Pinterest, Disqus, and Mozilla all use or have used Django.

The Django motto is:
> **"The web framework for perfectionists with deadlines."**

It takes care of many common tasks - user authentication, database management, URL routing, HTML templating, form handling, admin panels - so you can focus on the parts that make your application unique.

---

## 15.2 Why Django for This Course?

After learning OOP (Unit 2), databases (Unit 6), and networking (Unit 7), Django is the natural next step because it combines all three:

| Previous Unit | Django Component |
|---|---|
| Unit 2 - OOP | Models (Python classes that map to database tables) |
| Unit 6 - SQLite / Databases | ORM (Object-Relational Mapper - no SQL required) |
| Unit 7 - Network / Sockets | HTTP views and URL routing |
| Unit 8 - Threading | Django handles concurrency for you |

---

## 15.3 Django's Architecture - MVT

Django follows the **MVT (Model–View–Template)** pattern - a variation of the classic MVC pattern:

```
Browser Request
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────┐
│  URL     │────▶│  View    │────▶│ Template │
│ Routing  │     │(Logic)   │     │ (HTML)   │
└──────────┘     └────┬─────┘     └──────────┘
                      │
                 ┌────▼─────┐
                 │  Model   │
                 │(Database)│
                 └──────────┘
```

| Component | Responsibility | Django File |
|---|---|---|
| **Model** | Define the data structure; interact with the database | `models.py` |
| **View** | Handle HTTP requests; apply business logic; return responses | `views.py` |
| **Template** | HTML with placeholders; renders the final webpage | `templates/*.html` |
| **URL conf** | Map URL paths to view functions | `urls.py` |

---

## 15.4 The Django ORM - Models as Classes

A **Model** in Django is an OOP class that represents a database table. You never write SQL - Django generates it from your Python class.

```python
# models.py - defining a library database with Django

from django.db import models


class Student(models.Model):
    """Represents a registered library student."""
    name       = models.CharField(max_length=100)
    email      = models.EmailField(unique=True)
    enrolled   = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Book(models.Model):
    """Represents a book in the library catalogue."""
    title      = models.CharField(max_length=200)
    author     = models.CharField(max_length=100)
    isbn       = models.CharField(max_length=13, unique=True)
    copies     = models.IntegerField(default=1)
    added_on   = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class BorrowRecord(models.Model):
    """Records which student borrowed which book."""
    student    = models.ForeignKey(Student, on_delete=models.CASCADE)
    book       = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed   = models.DateField(auto_now_add=True)
    due_back   = models.DateField()
    returned   = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} → {self.book.title}"
```

**Django generates the SQL from this automatically.** You interact with your data using Python:

```python
# Querying with Django ORM - no SQL needed

# All books by a specific author
python_books = Book.objects.filter(author__icontains="Lutz")

# All students with overdue books
from django.utils import timezone
overdue = BorrowRecord.objects.filter(
    due_back__lt=timezone.now().date(),
    returned=False
)

# Create a new student
alice = Student.objects.create(name="Alice Smith", email="alice@uni.edu")

# Update a record
record = BorrowRecord.objects.get(id=1)
record.returned = True
record.save()
```

---

## 15.5 Views - Handling Requests

A **View** is a Python function (or class) that receives an HTTP request and returns an HTTP response.

```python
# views.py - library book search view

from django.shortcuts import render
from .models import Book


def book_search(request):
    """Search for books by title or author."""
    query   = request.GET.get("q", "")   # get the search term from URL
    results = []

    if query:
        results = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        )

    # Pass data to the template
    return render(request, "library/search.html", {
        "query":   query,
        "results": results,
    })
```

---

## 15.6 Templates - HTML with Django Tags

```html
<!-- templates/library/search.html -->

<h1>Library Search</h1>

<form method="get">
    <input type="text" name="q" value="{{ query }}">
    <button type="submit">Search</button>
</form>

{% if results %}
    <p>Found {{ results|length }} book(s):</p>
    <ul>
    {% for book in results %}
        <li>{{ book.title }} - {{ book.author }} ({{ book.copies }} copies)</li>
    {% endfor %}
    </ul>
{% elif query %}
    <p>No books found for "{{ query }}".</p>
{% endif %}
```

| Django Template Tag | Meaning |
|---|---|
| `{{ variable }}` | Output the value of a variable |
| `{% if ... %}` | Conditional block |
| `{% for ... in ... %}` | Loop |
| `{{ list\|length }}` | Apply a filter (like a function) to a variable |

---

## 15.7 URL Routing

```python
# urls.py - map URL paths to views

from django.urls import path
from . import views

urlpatterns = [
    path("",              views.home,        name="home"),
    path("search/",       views.book_search, name="search"),
    path("book/<int:id>/", views.book_detail, name="book-detail"),
]
```

A request to `/search/?q=Python` is routed to `book_search(request)`.  
A request to `/book/42/` is routed to `book_detail(request, id=42)`.

---

## 15.8 The Django Admin - Free Out of the Box

After registering your models, Django provides a **fully functional admin interface** at `/admin/` - no extra code required. Staff members can create, read, update, and delete records through a web browser.

```python
# admin.py

from django.contrib import admin
from .models import Student, Book, BorrowRecord

admin.site.register(Student)
admin.site.register(Book)
admin.site.register(BorrowRecord)
```

That is all - Django generates the admin UI automatically from your model definitions.

---

## 15.9 What Comes Next with Django

| Topic | Description |
|---|---|
| **Forms** | `forms.py` - validate user input before saving |
| **Authentication** | Built-in login, logout, registration, permissions |
| **REST API** | Django REST Framework - serve JSON instead of HTML |
| **Deployment** | Host on a server (Heroku, AWS, Azure, Vercel) |
| **Middleware** | Custom code that runs on every request |

---

---

# 16. Common Mistakes Reference

---

| # | Mistake | Wrong | Right |
|---|---|---|---|
| 1 | Forgetting `r""` for regex patterns | `re.split("\s+", t)` | `re.split(r"\s+", t)` |
| 2 | Discarding `sub()` result | `re.sub(r"X", "Y", text)` | `text = re.sub(r"X", "Y", text)` |
| 3 | Not joining threads | `t.start()` only | `t.start(); t.join()` |
| 4 | Assuming thread execution order | `print(result)` immediately after `t.start()` | Always `t.join()` first |
| 5 | Modifying shared data without a lock | `balance += 1` (in two threads) | `with lock: balance += 1` |
| 6 | Confusing `match()` and `search()` | Using `match()` to find text in the middle | Use `search()` for mid-string searching |
| 7 | Matching too broadly with `.` | `r"<.+>"` matches across tags | `r"<.+?>"` (non-greedy) |
| 8 | Forgetting `^` and `$` in validation | `r"\d{4}"` matches `99BT20249` | `r"^\d{4}$"` to match exactly |
| 9 | Not escaping literal dots | `r"\d+.\d{2}"` matches `£250X99` | `r"\d+\.\d{2}"` (escape the dot) |
| 10 | Unhandled exceptions in threads | Thread dies silently | Wrap with `try / except` |

---

# 17. Best Practices Summary

---

**Regular Expressions:**

1. **Always use raw strings** (`r"..."`) for regex patterns - without exception.
2. **Compile patterns** (`re.compile(...)`) that are used more than once in a loop.
3. **Use `^` and `$` anchors** when validating a complete string.
4. **Prefer named groups** (`(?P<name>...)`) over numbered groups for readability.
5. **Test patterns interactively** - use a tool like [regex101.com](https://regex101.com) during development.
6. **Use non-greedy quantifiers** (`*?`, `+?`) when matching between delimiters.
7. **Comment complex patterns** using `re.VERBOSE` mode.

```python
# re.VERBOSE allows whitespace and comments inside the pattern
email_pattern = re.compile(r"""
    [\w.\-]+    # local part: letters, dots, hyphens
    @           # the @ symbol
    [\w.\-]+    # domain name
    \.          # a literal dot
    [a-zA-Z]{2,} # TLD: at least 2 letters
""", re.VERBOSE)
```

**Threads:**

8. **Always join non-daemon threads** before the program exits.
9. **Always protect shared mutable state** with a `Lock`.
10. **Use `with lock:`** - never call `acquire()` and `release()` manually.
11. **Keep the critical section small** - only the code that accesses shared data needs the lock.
12. **Use daemon threads** for background helpers that should not block program exit.
13. **Wrap thread functions in `try / except`** - exceptions inside threads disappear silently.
14. **Use `threading.Event`** to signal between threads instead of global boolean flags.

---

# 18. Key Takeaways

---

## Regular Expressions

- A **regular expression** is a pattern that describes the shape of text you want to find or validate.
- Always use **raw strings** (`r"..."`) for patterns.
- `re.split()` splits on a **pattern**, not just a fixed character.
- `re.findall()` returns **all** matches; `re.search()` returns the **first** match anywhere.
- `re.match()` only checks the **start** of the string.
- `re.sub()` **replaces** matches and always returns a **new string**.
- **Quantifiers** control repetition: `*` (0+), `+` (1+), `?` (0 or 1), `{n}` (exactly n).
- **Character classes** `[...]` match any one character from the set.
- **Capturing groups** `(...)` extract parts of a match.
- **`\b`** (word boundary) prevents partial-word matches.

## Threads

- A **process** has its own memory; a **thread** shares memory with other threads in the same process.
- The **GIL** means Python threads do not speed up CPU-bound work - use `multiprocessing` for that.
- Threads are excellent for **I/O-bound** tasks (downloading, waiting for input, database queries).
- **Race conditions** occur when threads access shared data without synchronisation.
- A **Lock** (`threading.Lock`) ensures only one thread enters a critical section at a time.
- A **Semaphore** limits concurrent access to N threads.
- An **Event** lets threads signal each other.
- Thread life cycle: **New → Runnable → Running → Blocked → Terminated**.
- Use `daemon=True` for background threads that should auto-exit with the main program.

## Django

- Django follows **MVT**: Model (data), View (logic), Template (HTML).
- **Models** are Python classes - Django generates SQL from them automatically.
- The **ORM** lets you query the database in pure Python - no SQL required.
- The **admin interface** is generated automatically from model definitions.
- Django connects your OOP, database, and networking skills into one framework.

---

# 19. Unit Summary

---

## What We Covered

| Section | Topics |
|---|---|
| Part A | Regular expressions - `split()`, special characters, dates, emails, quantifiers, `match()`, `findall()`, character sequences, `sub()`, `search()` |
| Part B | Processes vs threads, `threading.Thread`, `Lock`, `Semaphore`, `Event`, thread life cycle |
| Part C | Django MVT, Models, ORM, Views, Templates, URL routing, Admin |

---

## The Conceptual Journey

```
Raw Text (messy, inconsistent)
         │
    re.findall() / re.sub()
         │
         ▼
Structured Data (extracted, cleaned)
         │
    Python objects / SQLite / Django Models
         │
         ▼
Application Logic (OOP classes, functions)
         │
    threading.Thread + Lock
         │
         ▼
Concurrent Execution (multiple users served at once)
         │
    Django Views + URL routing
         │
         ▼
HTTP Response (the web application)
```

Everything in this course has been building toward this moment. Regular expressions clean and extract data. Threads allow multiple users to be served simultaneously. Django brings them together into a complete web application.

---

## Quick-Reference Card

```python
import re
import threading

# ── Regular Expressions ───────────────────────────────────────────────────────
re.split(r"[,;\s]+", text)               # Split on multiple separators
re.findall(r"\d{2}/\d{2}/\d{4}", text)  # Find all dates
re.search(r"\bkeyword\b", text)         # Find keyword anywhere
re.match(r"^[A-Z]{2}\d{4}$", text)     # Validate from the start
re.sub(r"(\d{2})/(\d{2})/(\d{4})",
       r"\3-\2-\1", text)              # Rearrange date format

# ── Threads ───────────────────────────────────────────────────────────────────
lock = threading.Lock()

def worker():
    with lock:           # acquire and auto-release
        shared_data += 1 # critical section - safe

t = threading.Thread(target=worker, args=(), daemon=False)
t.start()
t.join()    # wait for completion

# ── Thread-safe class pattern ─────────────────────────────────────────────────
class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock  = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        with self._lock:
            return self._value
```

---

*End of Unit 8 Lecture Notes*  
*BT151CO - Object-Oriented Programming with Python*
