import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import json
import os

class GitHubLinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo & Guide Manager")
        self.root.geometry("800x600")
        
        # Danh sách repo và hướng dẫn
        self.data = {"repos": []}
        self.data_file = "repos.json"
        self.load_data()
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview để hiển thị danh sách
        columns = ("Repository", "Guide")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.tree.heading("Repository", text="Repository URL")
        self.tree.heading("Guide", text="Guide URL/File")
        self.tree.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=4, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame nhập liệu
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky=tk.W)
        
        ttk.Label(input_frame, text="Repo URL:").grid(row=0, column=0, padx=5)
        self.repo_entry = ttk.Entry(input_frame, width=50)
        self.repo_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Guide URL/File:").grid(row=1, column=0, padx=5)
        self.guide_entry = ttk.Entry(input_frame, width=50)
        self.guide_entry.grid(row=1, column=1, padx=5)
        
        # Frame nút
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add Repo", command=self.add_repo).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_repo).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Open Repo", command=self.open_repo).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Open Guide", command=self.open_guide).grid(row=0, column=3, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=3, column=0, columnspan=4, sticky=tk.W)
        
        # Load dữ liệu vào Treeview
        self.refresh_treeview()
        
    def load_data(self):
        # Load dữ liệu từ file JSON nếu tồn tại
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.data = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
                
    def save_data(self):
        # Lưu dữ liệu vào file JSON
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            
    def refresh_treeview(self):
        # Xóa Treeview hiện tại
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Thêm dữ liệu mới
        for repo in self.data["repos"]:
            self.tree.insert("", tk.END, values=(repo["url"], repo["guide"]))
            
    def add_repo(self):
        repo_url = self.repo_entry.get().strip()
        guide = self.guide_entry.get().strip()
        
        if not repo_url or not guide:
            messagebox.showwarning("Warning", "Please fill in both fields")
            return
            
        # Kiểm tra định dạng URL repo (cơ bản)
        if not repo_url.startswith("https://github.com"):
            messagebox.showwarning("Warning", "Please enter a valid GitHub repository URL")
            return
            
        # Thêm vào danh sách
        self.data["repos"].append({"url": repo_url, "guide": guide})
        self.save_data()
        self.refresh_treeview()
        
        # Xóa input
        self.repo_entry.delete(0, tk.END)
        self.guide_entry.delete(0, tk.END)
        self.status_var.set("Repository added successfully")
        
    def delete_repo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a repository to delete")
            return
            
        # Xóa mục được chọn
        selected_item = self.tree.item(selected[0])["values"]
        self.data["repos"] = [repo for repo in self.data["repos"] if repo["url"] != selected_item[0]]
        self.save_data()
        self.refresh_treeview()
        self.status_var.set("Repository deleted successfully")
        
    def open_repo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a repository")
            return
            
        repo_url = self.tree.item(selected[0])["values"][0]
        try:
            webbrowser.open(repo_url)
            self.status_var.set("Opened repository in browser")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open repository: {str(e)}")
            
    def open_guide(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a repository")
            return
            
        guide = self.tree.item(selected[0])["values"][1]
        try:
            if guide.startswith("http"):
                webbrowser.open(guide)
            else:
                # Nếu là file local
                os.startfile(guide) if os.name == "nt" else os.system(f"open {guide}")
            self.status_var.set("Opened guide")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open guide: {str(e)}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubLinkApp(root)
    root.mainloop()
