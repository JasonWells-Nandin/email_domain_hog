import re
import tkinter as tk
from tkinter import filedialog
from openpyxl import load_workbook
import json

# Function to check the data type of input
def check_input(input_data):
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    domain_pattern = r'^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$'
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(ip_pattern, input_data):
        return "IP Address"
    elif re.match(domain_pattern, input_data):
        return "Domain Name"
    elif re.match(email_pattern, input_data):
        return "Email Address"
    else:
        return "Unidentified"

# Function to process manually entered data
def process_input():
    data = entry.get()
    if data:
        label = check_input(data)
        result_label.config(text="Input Data: {}\nData Type: {}".format(data, label))

# Function to handle file selection
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                output = ""
                results = []
                for line in file:
                    line = line.strip()
                    label = check_input(line)
                    results.append({"Input Data": line, "Data Type": label})
                    output += "Input Data: {}\nData Type: {}\n\n".format(line, label)
                result_label.config(text=output)
                return results
        elif file_path.endswith('.xlsx'):
            wb = load_workbook(file_path)
            sheet = wb.active
            output = ""
            results = []
            for row in sheet.iter_rows(values_only=True):
                for cell in row:
                    label = check_input(str(cell))
                    results.append({"Input Data": cell, "Data Type": label})
                    output += "Input Data: {}\nData Type: {}\n\n".format(cell, label)
            result_label.config(text=output)
            return results
        else:
            result_label.config(text="Unsupported file type")

# Export results to a JSON file at the specified path
def export_to_json(results):
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, ensure_ascii=False, indent=4)

# Main function
def main():
    root = tk.Tk()
    root.title("Data Classification Tool")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    entry_label = tk.Label(frame, text="Enter data to check:")
    entry_label.grid(row=0, column=0)

    global entry
    entry = tk.Entry(frame, width=50)
    entry.grid(row=0, column=1)

    process_button = tk.Button(frame, text="Check", command=process_input)
    process_button.grid(row=0, column=2, padx=5)

    file_button = tk.Button(frame, text="Browse File", command=lambda: handle_file_selection(browse_file()))
    file_button.grid(row=0, column=3, padx=5)

    global result_label
    result_label = tk.Label(root, text="", justify="left")
    result_label.pack(pady=10)

    root.mainloop()

# Function to handle input data in CLI mode
def cli_mode():
    while True:
        data = input("Enter data to check (enter q to quit): ")
        if data.lower() == 'q':
            break
        label = check_input(data)
        print("Input Data:", data)
        print("Data Type:", label)
        print()

# Function to handle file selection results
def handle_file_selection(results):
    if results:
        export_choice = tk.messagebox.askyesno("Export to JSON", "Would you like to export to a JSON file?")
        if export_choice:
            export_to_json(results)

if __name__ == "__main__":
    main()
    print("\nEntering CLI Mode:\n")
    cli_mode()
