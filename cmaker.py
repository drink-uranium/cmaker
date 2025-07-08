import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import tempfile
import shutil
import re

cloned_path = None  # Stores the path of the cloned repo

def import_folder():
    global cloned_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        import_button.config(text="Imported", state="normal")
        import_button.folder_path = folder_path
        cloned_path = None  # Clear any cloned path
        url_entry.config(state="normal")
        build_button.config(state="normal")

def output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_button.config(text="Set")
        output_button.folder_path = folder_path

def is_github_url(url):
    return re.match(r'^https:\/\/github\.com\/[\w\-]+\/[\w\-]+', url.strip())

def fetch_repo():
    global cloned_path
    url = url_entry.get().strip()
    if not is_github_url(url):
        messagebox.showerror("Invalid URL", "Please enter a valid GitHub repo URL.")
        return

    try:
        tmp_dir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", url, tmp_dir], check=True)
        cloned_path = tmp_dir

        # Update UI states
        url_entry.config(state="disabled")
        import_button.config(state="disabled", text="Disabled")
        import_button.folder_path = None
        build_button.config(state="normal")

        messagebox.showinfo("Cloned", f"Repository cloned to:\n{tmp_dir}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Clone Failed", "Failed to clone GitHub repository.")

def build_project():
    try:
        folder = cloned_path or getattr(import_button, 'folder_path', None)
        out_dir = getattr(output_button, 'folder_path', None)

        if not folder:
            messagebox.showerror("Error", "No source folder set.")
            return

        os.chdir(folder)

        # Run build based on detected system
        if os.path.exists("Makefile"):
            subprocess.run(["make"], check=True)
        elif os.path.exists("SConstruct"):
            subprocess.run(["scons"], check=True)
        elif os.path.exists("CMakeLists.txt"):
            build_dir = os.path.join(folder, "build")
            os.makedirs(build_dir, exist_ok=True)
            subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
            subprocess.run(["make"], cwd=build_dir, check=True)
            folder = build_dir  # Use build dir for output search
        else:
            messagebox.showerror("No Build System", "No Makefile, SConstruct, or CMakeLists.txt found.")
            return

        if out_dir:
            # Search for executables in build folder
            moved = False
            found_execs = []

            for name in os.listdir(folder):
                path = os.path.join(folder, name)
                if os.path.isfile(path) and os.access(path, os.X_OK):
                    # Ignore known non-binary file types
                    if not name.endswith((".cmake", ".sh")):
                        shutil.copy2(path, os.path.join(out_dir, name))
                        messagebox.showinfo("Build Complete", f"Binary copied to:\n{os.path.join(out_dir, name)}")
                        moved = True
                        break
                    else:
                        found_execs.append(name)

            if not moved:
                # Try to show what executables were found
                for name in os.listdir(folder):
                    path = os.path.join(folder, name)
                    if os.path.isfile(path) and os.access(path, os.X_OK):
                        found_execs.append(name)

                if found_execs:
                    messagebox.showwarning("Build Done", "Build completed, but binary not identified.\n"
                                          "Executables found:\n" + "\n".join(found_execs))
                else:
                    messagebox.showwarning("Build Done", "Build completed, but no executables found.")
        else:
            messagebox.showinfo("Build Complete", "Build finished in source directory.")

    except subprocess.CalledProcessError:
        messagebox.showerror("Build Failed", "Build command failed. Check your source code.")

# GUI Setup
root = tk.Tk()
root.title("automatic source code builder")
root.configure(bg="#1e1e1e")
root.geometry("640x432")  # Simulate 80x24 terminal
root.resizable(False, False)

# Title
label = tk.Label(root, text="automatic source\ncode builder", font=("Helvetica", 18, "bold"),
                 fg="white", bg="#1e1e1e", justify="center")
label.pack(pady=20)

# GitHub URL Entry
url_frame = tk.Frame(root, bg="#1e1e1e")
url_frame.pack()

url_entry = tk.Entry(url_frame, width=40, font=("Courier", 12))
url_entry.pack(side="left", padx=5)

clone_button = tk.Button(url_frame, text="Clone", command=fetch_repo,
                         font=("Helvetica", 10, "bold"), bg="#007acc", fg="white",
                         activebackground="#007acc", width=8)
clone_button.pack(side="left", padx=5)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=30)

def styled_button(master, text, command, color):
    return tk.Button(master, text=text, command=command,
                     font=("Helvetica", 12, "bold"), fg="white",
                     bg=color, activebackground=color,
                     width=10, height=2, bd=0, relief="flat")

import_button = styled_button(btn_frame, "Import", import_folder, "#0099ff")
import_button.grid(row=0, column=0, padx=10)

output_button = styled_button(btn_frame, "Output", output_folder, "#0099ff")
output_button.grid(row=0, column=1, padx=10)

build_button = styled_button(btn_frame, "Build", build_project, "#00cc44")
build_button.grid(row=0, column=2, padx=10)
build_button.config(state="disabled")

root.mainloop()
