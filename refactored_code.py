import tkinter as tk
from tkinter import messagebox

class SmartToDoTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart ToDoTracker")

        # Create user interface components
        self.label = tk.Label(root, text="Smart ToDoTracker", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.add_item_label = tk.Label(root, text="Add Item:")
        self.add_item_label.pack(pady=5)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Add", command=self.add_item)
        self.add_button.pack(pady=5)

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.remove_button = tk.Button(root, text="Remove Selected", command=self.remove_item)
        self.remove_button.pack(pady=5)

    def add_item(self):
        """Add an item to the listbox from the entry field."""
        item = self.entry.get().strip()  # Stripping whitespace
        if item:  # Ensures that the item is not just spaces
            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END)  # Clear the entry field after adding
        else:
            messagebox.showwarning("Warning", "Please enter an item to add.")

    def remove_item(self):
        """Remove selected item from the listbox."""
        try:
            selected_index = self.listbox.curselection()[0]
            self.listbox.delete(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item to remove.")

def main():
    root = tk.Tk()
    app = SmartToDoTrackerApp(root)
    root.geometry("300x400")  # Set the size of the application window
    root.mainloop()

# Test cases based on router recommendations
def test_smart_todo_tracker_app():
    """Test cases to verify application functionality."""
    # Test setup
    root = tk.Tk()
    app = SmartToDoTrackerApp(root)

    # Test adding an item
    app.entry.insert(0, "Test Item")
    app.add_item()
    assert app.listbox.get(0) == "Test Item", "Failed: Item was not added correctly."

    # Test removing an item
    app.listbox.select_set(0)  # Select the first item
    app.remove_item()
    assert app.listbox.size() == 0, "Failed: Item was not removed correctly."

    # Test empty input handle
    app.entry.insert(0, "")
    app.add_item()  # Should show warning
    # This cannot be asserted since it would require GUI observation, but we can ensure no exception is raised.

    # Edge case: Attempt to remove from empty list
    app.remove_item()  # Should show warning

    print("All test cases passed successfully!")

if __name__ == "__main__":
    main()
    test_smart_todo_tracker_app()