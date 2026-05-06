import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class SafeZoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeZone - Area Safety & Reporting")
        self.root.geometry("800x600")
        
        self.db = Database()
        if not self.db.is_connected():
            messagebox.showerror("Database Error", "Could not connect to MySQL Database. Please check your credentials and ensure the server is running.")
            
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        self.create_dashboard_tab()
        self.create_explore_tab()
        self.create_report_tab()
        self.create_view_reports_tab()
        self.create_admin_tab()
        
        self.refresh_areas_comboboxes()
        
        # We'll use a style for better look
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        
    def create_dashboard_tab(self):
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_dashboard, text='Dashboard')
        
        ttk.Label(self.tab_dashboard, text="SafeZone Dashboard", font=("Helvetica", 18, "bold")).pack(pady=20)
        
        # Area Selection
        select_frame = ttk.Frame(self.tab_dashboard)
        select_frame.pack(pady=10)
        
        ttk.Label(select_frame, text="Select Area: ", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.dash_area_var = tk.StringVar()
        self.dash_area_cb = ttk.Combobox(select_frame, textvariable=self.dash_area_var, state='readonly', width=30)
        self.dash_area_cb.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(select_frame, text="View Summary", command=self.load_dashboard_summary).pack(side=tk.LEFT)
        
        # Summary Frame
        self.summary_frame = ttk.LabelFrame(self.tab_dashboard, text="Safety Summary", padding=(20, 10))
        self.summary_frame.pack(pady=20, fill="x", padx=50)
        
        self.lbl_score = ttk.Label(self.summary_frame, text="Safety Score: --", font=("Helvetica", 12))
        self.lbl_score.pack(anchor="w", pady=5)
        
        self.lbl_status = ttk.Label(self.summary_frame, text="Status: --", font=("Helvetica", 12))
        self.lbl_status.pack(anchor="w", pady=5)
        
        self.lbl_total_reports = ttk.Label(self.summary_frame, text="Total Reports (Last 30 Days): --", font=("Helvetica", 12))
        self.lbl_total_reports.pack(anchor="w", pady=5)
        
        self.lbl_common_type = ttk.Label(self.summary_frame, text="Most Common Incident: --", font=("Helvetica", 12))
        self.lbl_common_type.pack(anchor="w", pady=5)

    def create_explore_tab(self):
        self.tab_explore = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_explore, text='Explore Areas')
        
        ttk.Label(self.tab_explore, text="Explore Areas", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        columns = ("Area Name", "City", "Safety Status", "Score")
        self.tree_explore = ttk.Treeview(self.tab_explore, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree_explore.heading(col, text=col)
            self.tree_explore.column(col, width=150, anchor="center")
            
        self.tree_explore.pack(pady=10, fill="x", padx=20)
        
        ttk.Button(self.tab_explore, text="Refresh Data", command=self.load_explore_data).pack(pady=10)
        self.load_explore_data()

    def create_report_tab(self):
        self.tab_report = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_report, text='Report an Area')
        
        ttk.Label(self.tab_report, text="Submit a Safety Report", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        form_frame = ttk.Frame(self.tab_report)
        form_frame.pack(pady=10)
        
        # Area
        ttk.Label(form_frame, text="Area:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.report_area_var = tk.StringVar()
        self.report_area_cb = ttk.Combobox(form_frame, textvariable=self.report_area_var, state='readonly', width=30)
        self.report_area_cb.grid(row=0, column=1, pady=5, padx=5)
        
        # Incident Type
        ttk.Label(form_frame, text="Incident Type:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.incident_var = tk.StringVar()
        incident_types = ["Theft", "Harassment", "Accident", "Violence", "Scam", "Other"]
        ttk.Combobox(form_frame, textvariable=self.incident_var, values=incident_types, state='readonly', width=30).grid(row=1, column=1, pady=5, padx=5)
        
        # Severity
        ttk.Label(form_frame, text="Severity (1-5):").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.severity_var = tk.StringVar()
        ttk.Combobox(form_frame, textvariable=self.severity_var, values=["1", "2", "3", "4", "5"], state='readonly', width=10).grid(row=2, column=1, sticky="w", pady=5, padx=5)
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky="ne", pady=5, padx=5)
        self.desc_text = tk.Text(form_frame, width=40, height=5)
        self.desc_text.grid(row=3, column=1, pady=5, padx=5)
        
        # Reporter Name
        ttk.Label(form_frame, text="Your Name (Optional):").grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.reporter_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.reporter_name_var, width=32).grid(row=4, column=1, sticky="w", pady=5, padx=5)
        
        # Submit Button
        ttk.Button(form_frame, text="Submit Report", command=self.submit_report).grid(row=5, column=0, columnspan=2, pady=20)

    def create_view_reports_tab(self):
        self.tab_view = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_view, text='View Reports')
        
        ttk.Label(self.tab_view, text="Recent Area Reports", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        select_frame = ttk.Frame(self.tab_view)
        select_frame.pack(pady=10)
        
        ttk.Label(select_frame, text="Select Area:").pack(side=tk.LEFT)
        self.view_area_var = tk.StringVar()
        self.view_area_cb = ttk.Combobox(select_frame, textvariable=self.view_area_var, state='readonly', width=30)
        self.view_area_cb.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(select_frame, text="Load Reports", command=self.load_reports).pack(side=tk.LEFT)
        
        columns = ("Type", "Severity", "Time", "Description")
        self.tree_reports = ttk.Treeview(self.tab_view, columns=columns, show="headings", height=15)
        self.tree_reports.heading("Type", text="Incident Type")
        self.tree_reports.column("Type", width=100)
        self.tree_reports.heading("Severity", text="Severity")
        self.tree_reports.column("Severity", width=80, anchor="center")
        self.tree_reports.heading("Time", text="Date/Time")
        self.tree_reports.column("Time", width=150)
        self.tree_reports.heading("Description", text="Description")
        self.tree_reports.column("Description", width=400)
        
        self.tree_reports.pack(pady=10, fill="x", padx=20)

    def create_admin_tab(self):
        self.tab_admin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_admin, text='Admin')
        
        # Login Frame
        self.login_frame = ttk.Frame(self.tab_admin)
        self.login_frame.pack(pady=50)
        
        ttk.Label(self.login_frame, text="Admin Login", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.admin_user_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.admin_user_var).pack(pady=5)
        
        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.admin_pass_var = tk.StringVar()
        ttk.Entry(self.login_frame, textvariable=self.admin_pass_var, show="*").pack(pady=5)
        
        ttk.Button(self.login_frame, text="Login", command=self.admin_login).pack(pady=20)
        
        # Admin Dashboard Frame (hidden by default)
        self.admin_dash = ttk.Frame(self.tab_admin)
        
        ttk.Label(self.admin_dash, text="Admin Dashboard - Moderation not fully implemented in this demo", font=("Helvetica", 12)).pack(pady=20)
        ttk.Button(self.admin_dash, text="Logout", command=self.admin_logout).pack(pady=10)

    def refresh_areas_comboboxes(self):
        areas = self.db.fetch_all_areas()
        area_names = [a['area_name'] for a in areas]
        self.dash_area_cb['values'] = area_names
        self.report_area_cb['values'] = area_names
        self.view_area_cb['values'] = area_names

    def load_dashboard_summary(self):
        area_name = self.dash_area_var.get()
        if not area_name:
            messagebox.showwarning("Input Error", "Please select an area.")
            return
            
        area = self.db.fetch_area_by_name(area_name)
        if area:
            summary = self.db.get_area_summary(area['area_id'])
            if summary:
                self.lbl_score.config(text=f"Safety Score: {summary['score']}/100")
                self.lbl_status.config(text=f"Status: {summary['status']}")
                self.lbl_total_reports.config(text=f"Total Reports (Last 30 Days): {summary['total_reports_30d']}")
                self.lbl_common_type.config(text=f"Most Common Incident: {summary['most_common_type']}")
                
                # Update status color
                if summary['status'] == 'Safe':
                    self.lbl_status.config(foreground="green")
                elif summary['status'] == 'Moderate':
                    self.lbl_status.config(foreground="orange")
                else:
                    self.lbl_status.config(foreground="red")

    def load_explore_data(self):
        # Clear existing
        for item in self.tree_explore.get_children():
            self.tree_explore.delete(item)
            
        areas = self.db.fetch_all_areas()
        for a in areas:
            self.tree_explore.insert("", "end", values=(a['area_name'], a['city'], a['current_status'], a['current_score']))

    def submit_report(self):
        area_name = self.report_area_var.get()
        incident_type = self.incident_var.get()
        severity = self.severity_var.get()
        desc = self.desc_text.get("1.0", tk.END).strip()
        reporter = self.reporter_name_var.get()
        
        if not all([area_name, incident_type, severity, desc]):
            messagebox.showwarning("Missing Fields", "Please fill out all required fields (Area, Type, Severity, Description).")
            return
            
        area = self.db.fetch_area_by_name(area_name)
        if area:
            success = self.db.add_report(area['area_id'], incident_type, int(severity), desc, reporter, "")
            if success:
                messagebox.showinfo("Success", "Report submitted successfully! The area safety score has been updated.")
                self.desc_text.delete("1.0", tk.END)
                self.incident_var.set("")
                self.severity_var.set("")
                self.report_area_var.set("")
                self.reporter_name_var.set("")
                # Refresh data
                self.load_explore_data()
            else:
                messagebox.showerror("Error", "Failed to submit report.")

    def load_reports(self):
        for item in self.tree_reports.get_children():
            self.tree_reports.delete(item)
            
        area_name = self.view_area_var.get()
        if not area_name:
            return
            
        area = self.db.fetch_area_by_name(area_name)
        if area:
            reports = self.db.fetch_reports_by_area(area['area_id'])
            for r in reports:
                self.tree_reports.insert("", "end", values=(r['incident_type'], r['severity'], r['report_time'], r['description']))

    def admin_login(self):
        user = self.admin_user_var.get()
        pwd = self.admin_pass_var.get()
        
        if self.db.verify_admin(user, pwd):
            self.login_frame.pack_forget()
            self.admin_dash.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def admin_logout(self):
        self.admin_user_var.set("")
        self.admin_pass_var.set("")
        self.admin_dash.pack_forget()
        self.login_frame.pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = SafeZoneApp(root)
    root.mainloop()
