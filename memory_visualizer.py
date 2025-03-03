# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==============================================
# MODULE 1: MEMORY TRACKER (Team Member B)
# ==============================================
class MemoryBlock:
    def __init__(self, start, size, status="free"):
        self.start = start
        self.size = size
        self.status = status
        self.freed = False  # For leak detection

class MemoryTracker:
    def __init__(self, heap_size=1024):
        self.heap = [MemoryBlock(0, heap_size, "free")]
        self.allocations = {}  # Track allocated blocks by address

    def allocate(self, size):
        # First-fit allocation strategy
        for i, block in enumerate(self.heap):
            if block.status == "free" and block.size >= size:
                # Split the block
                new_block = MemoryBlock(block.start, size, "allocated")
                remaining_size = block.size - size
                if remaining_size > 0:
                    remaining_block = MemoryBlock(block.start + size, remaining_size, "free")
                    self.heap.insert(i + 1, remaining_block)
                self.heap[i] = new_block
                self.allocations[new_block.start] = new_block
                return new_block.start
        return None  # No space

    def free(self, address):
        if address not in self.allocations:
            return "Invalid address"
        block = self.allocations[address]
        block.status = "free"
        block.freed = True
        # Merge adjacent free blocks
        self._merge_blocks()
        return "Freed successfully"

    def _merge_blocks(self):
        i = 0
        while i < len(self.heap) - 1:
            curr = self.heap[i]
            next_block = self.heap[i + 1]
            if curr.status == "free" and next_block.status == "free":
                curr.size += next_block.size
                del self.heap[i + 1]
            else:
                i += 1

    def get_leaks(self):
        return [block for block in self.heap if block.status == "allocated" and not block.freed]

# ==============================================
# MODULE 2: GUI (Team Member A)
# ==============================================
class MemoryVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Memory Visualizer")
        self.tracker = MemoryTracker(heap_size=1024)
        
        # GUI Components
        self.size_label = tk.Label(root, text="Size:")
        self.size_entry = tk.Entry(root)
        self.allocate_btn = tk.Button(root, text="Allocate", command=self.allocate)
        self.address_label = tk.Label(root, text="Address to Free:")
        self.address_entry = tk.Entry(root)
        self.free_btn = tk.Button(root, text="Free", command=self.free)
        self.status_label = tk.Label(root, text="Status: Ready")
        
        # Visualization Canvas (Matplotlib)
        self.fig, self.ax = plt.subplots(figsize=(10, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.draw_heap()
        
        # Layout
        self.size_label.grid(row=0, column=0, padx=5, pady=5)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)
        self.allocate_btn.grid(row=0, column=2, padx=5, pady=5)
        self.address_label.grid(row=1, column=0, padx=5, pady=5)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5)
        self.free_btn.grid(row=1, column=2, padx=5, pady=5)
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)

    def allocate(self):
        try:
            size = int(self.size_entry.get())
            address = self.tracker.allocate(size)
            if address is None:
                self.status_label.config(text="Status: Allocation failed (not enough space)")
            else:
                self.status_label.config(text=f"Status: Allocated {size} bytes at address {address}")
            self.draw_heap()
        except ValueError:
            messagebox.showerror("Error", "Invalid size")

    def free(self):
        try:
            address = int(self.address_entry.get())
            result = self.tracker.free(address)
            self.status_label.config(text=f"Status: {result}")
            self.draw_heap()
        except ValueError:
            messagebox.showerror("Error", "Invalid address")

    def draw_heap(self):
        self.ax.clear()
        for block in self.tracker.heap:
            color = "green" if block.status == "allocated" else "red"
            self.ax.barh(0, block.size, left=block.start, color=color, edgecolor="black")
        self.ax.set_xlim(0, 1024)
        self.ax.set_xticks(range(0, 1025, 128))
        self.ax.set_yticks([])
        self.canvas.draw()

# ==============================================
# MODULE 3: VISUALIZATION ENGINE (Team Member C)
# ==============================================
# (Integrated into the GUI class above)

# ==============================================
# RUN THE APPLICATION
# ==============================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizerGUI(root)
    root.mainloop()