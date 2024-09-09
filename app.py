import sys
import os
import time
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Increase recursion limit
sys.setrecursionlimit(1500)

# Ensure 'static' directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Function to generate random array
def generate_numbers(n):
    return [random.randint(1, 10000) for _ in range(n)]

# Sorting algorithms (Iterative and Recursive versions)
def iterative_selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def recursive_selection_sort(arr, start=0):
    if len(arr) > 1000:
        return iterative_selection_sort(arr)
    if start >= len(arr) - 1:
        return arr
    min_idx = start
    for i in range(start + 1, len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
    arr[start], arr[min_idx] = arr[min_idx], arr[start]
    return recursive_selection_sort(arr, start + 1)

def iterative_insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def recursive_insertion_sort(arr, n=None):
    if n is None:
        n = len(arr)
    if n > 1000:
        return iterative_insertion_sort(arr)
    if n <= 1:
        return arr
    recursive_insertion_sort(arr, n - 1)
    key = arr[n - 1]
    j = n - 2
    while j >= 0 and key < arr[j]:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = key
    return arr

def iterative_bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def recursive_bubble_sort(arr, n=None):
    if n is None:
        n = len(arr)
    if n > 1000:
        return iterative_bubble_sort(arr)
    if n == 1:
        return arr
    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return recursive_bubble_sort(arr, n - 1)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def iterative_merge_sort(arr):
    width = 1
    n = len(arr)
    while width < n:
        for i in range(0, n, 2 * width):
            left = arr[i:i + width]
            right = arr[i + width:i + 2 * width]
            merged = merge(left, right)
            arr[i:i + len(merged)] = merged
        width *= 2
    return arr

def recursive_merge_sort(arr):
    if len(arr) > 1000:
        return iterative_merge_sort(arr)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = recursive_merge_sort(arr[:mid])
    right = recursive_merge_sort(arr[mid:])
    return merge(left, right)

# Function to measure execution time
def measure_time(func, arr):
    start = time.time()
    sorted_arr = func(arr.copy())
    end = time.time()
    return end - start, sorted_arr

# Function to compare sorting algorithms and plot results
def compare_sorts(input_method, input_size, manual_input):
    sizes = [100, 500, 1000, 2000, 5000]
    times = {
        "Selection Sort (Iterative)": [],
        "Selection Sort (Recursive)": [],
        "Insertion Sort (Iterative)": [],
        "Insertion Sort (Recursive)": [],
        "Bubble Sort (Iterative)": [],
        "Bubble Sort (Recursive)": [],
        "Merge Sort (Iterative)": [],
        "Merge Sort (Recursive)": []
    }

    for n in sizes:
        if input_method == "random":
            arr = generate_numbers(n)
        elif input_method == "manual":
            arr = list(map(int, manual_input.split(',')))
        else:
            return

        times["Selection Sort (Iterative)"].append(measure_time(iterative_selection_sort, arr)[0])
        times["Selection Sort (Recursive)"].append(measure_time(recursive_selection_sort, arr)[0])
        times["Insertion Sort (Iterative)"].append(measure_time(iterative_insertion_sort, arr)[0])
        times["Insertion Sort (Recursive)"].append(measure_time(recursive_insertion_sort, arr)[0])
        times["Bubble Sort (Iterative)"].append(measure_time(iterative_bubble_sort, arr)[0])
        times["Bubble Sort (Recursive)"].append(measure_time(recursive_bubble_sort, arr)[0])
        times["Merge Sort (Iterative)"].append(measure_time(iterative_merge_sort, arr)[0])
        times["Merge Sort (Recursive)"].append(measure_time(recursive_merge_sort, arr)[0])

    # Plotting individual algorithm times
    for algo in times.keys():
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times[algo], label=algo, marker='o')
        plt.xlabel('Number of Elements')
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'{algo} Execution Time')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'static/{algo.replace(" ", "_")}_plot.png')
        plt.close()

    # Plotting Iterative vs Recursive comparisons
    for base_algo in ["Selection Sort", "Insertion Sort", "Bubble Sort", "Merge Sort"]:
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, times[f"{base_algo} (Iterative)"], label=f'{base_algo} (Iterative)', marker='o', linestyle='-')
        plt.plot(sizes, times[f"{base_algo} (Recursive)"], label=f'{base_algo} (Recursive)', marker='o', linestyle='--')
        plt.xlabel('Number of Elements')
        plt.ylabel('Execution Time (seconds)')
        plt.title(f'{base_algo} Iterative vs Recursive Comparison')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'static/{base_algo.replace(" ", "_")}_comparison_plot.png')
        plt.close()

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    input_method = request.form.get('input_method')
    input_size = int(request.form.get('size', 100))
    manual_input = request.form.get('manual_input', '')

    compare_sorts(input_method, input_size, manual_input)

    return redirect(url_for('show_results'))

@app.route('/results')
def show_results():
    images = [
        'Selection_Sort_(Iterative)_plot.png',
        'Selection_Sort_(Recursive)_plot.png',
        'Insertion_Sort_(Iterative)_plot.png',
        'Insertion_Sort_(Recursive)_plot.png',
        'Bubble_Sort_(Iterative)_plot.png',
        'Bubble_Sort_(Recursive)_plot.png',
        'Merge_Sort_(Iterative)_plot.png',
        'Merge_Sort_(Recursive)_plot.png',
        'Selection_Sort_comparison_plot.png',
        'Insertion_Sort_comparison_plot.png',
        'Bubble_Sort_comparison_plot.png',
        'Merge_Sort_comparison_plot.png'
    ]
    return render_template('results.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
