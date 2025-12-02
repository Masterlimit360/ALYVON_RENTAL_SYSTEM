"""
Improved rental management system with Ghana Cedis currency and multiple item support.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date, timedelta
from database import SessionLocal, Item, Customer, Rental, init_database
from sqlalchemy.orm import Session
from sqlalchemy import func
from PIL import Image, ImageTk
import os
import json
import shutil

# Import receipt and SMS modules
try:
    from receipt_generator import ReceiptGenerator
    from sms_sender import SMSSender
    from sms_config import get_sms_config, COMPANY_NAME, COMPANY_PHONE, COMPANY_EMAIL, COMPANY_ADDRESS, SMS_ENABLED
    RECEIPT_AVAILABLE = True
except ImportError as e:
    print(f"Receipt/SMS modules not available: {e}")
    RECEIPT_AVAILABLE = False

class RentalManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALYVON Rental Management System")
        self.root.geometry("1400x850")
        # Ensure window doesn't go below taskbar
        self.root.update_idletasks()
        screen_height = self.root.winfo_screenheight()
        taskbar_height = 50  # Approximate taskbar height
        max_height = screen_height - taskbar_height - 50
        if self.root.winfo_height() > max_height:
            self.root.geometry(f"1400x{max_height}")
        # Modern color scheme
        self.root.configure(bg='#f5f7fa')
        
        # Set window icon
        try:
            self.root.iconbitmap("ALYVON logo.ico")
        except:
            try:
                self.root.iconbitmap("ALYVON logo.png")
            except:
                pass
        
        # Initialize database
        init_database()
        
        # Rental items list for multiple item support
        self.rental_items = []
        
        # Create main interface
        self.create_widgets()
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Modern header with gradient effect
        header_frame = tk.Frame(self.root, bg='#1a237e', height=90)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Try to load and display logo
        try:
            logo_image = Image.open("ALYVON logo.png")
            logo_image = logo_image.resize((65, 65), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(header_frame, image=self.logo_photo, bg='#1a237e')
            logo_label.pack(side='left', padx=15, pady=12)
        except:
            # If logo fails to load, just show text
            logo_label = tk.Label(header_frame, text="ALYVON", font=("Segoe UI", 18, "bold"), 
                                fg='white', bg='#1a237e')
            logo_label.pack(side='left', padx=15, pady=12)
        
        # Title with better styling
        title_label = tk.Label(header_frame, text="Rental Management System", 
                              font=("Segoe UI", 18, "bold"), fg='white', bg='#1a237e')
        title_label.pack(side='left', padx=25, pady=12)
        
        # Currency label with modern styling
        currency_label = tk.Label(header_frame, text="Currency: Ghana Cedis (GHS)", 
                                font=("Segoe UI", 10), fg='#e3f2fd', bg='#1a237e')
        currency_label.pack(side='right', padx=25, pady=12)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        try:
            self.create_dashboard_tab()
            self.create_rental_tab()
            self.create_inventory_tab()
            self.create_customers_tab()
            self.create_rentals_tab()
            self.create_reports_tab()
            self.create_history_tab()
            
            # Load initial data
            self.refresh_dashboard()
            self.refresh_inventory()
            self.refresh_rentals()
            self.refresh_customers()
            self.refresh_history()
        except Exception as e:
            print(f"Application initialization error: {e}")
            messagebox.showerror("Error", f"Failed to initialize application: {e}")
        
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Dashboard content with modern styling
        title_label = tk.Label(dashboard_frame, text="Rental System Overview", 
                font=("Segoe UI", 16, "bold"), fg='#1a237e', bg='#f5f7fa')
        title_label.pack(pady=15)
        
        # Summary frame with modern card design
        summary_frame = tk.Frame(dashboard_frame, bg='white', relief='flat', bd=0)
        summary_frame.pack(fill='x', padx=20, pady=10)
        # Add subtle border effect
        border_frame = tk.Frame(summary_frame, bg='#e0e0e0', height=1)
        border_frame.pack(fill='x', side='bottom')
        
        # Create summary labels as instance variables for refresh
        self.total_items_label = tk.Label(summary_frame, text="Total Items: 0", 
                font=("Arial", 12), bg='white')
        self.total_items_label.pack(anchor='w', padx=10, pady=5)
        
        self.total_customers_label = tk.Label(summary_frame, text="Total Customers: 0", 
                font=("Arial", 12), bg='white')
        self.total_customers_label.pack(anchor='w', padx=10, pady=5)
        
        self.active_rentals_label = tk.Label(summary_frame, text="Active Rentals: 0", 
                font=("Arial", 12), bg='white')
        self.active_rentals_label.pack(anchor='w', padx=10, pady=5)
        
        self.total_revenue_label = tk.Label(summary_frame, text="Total Revenue: GHS 0.00", 
                font=("Arial", 12), bg='white')
        self.total_revenue_label.pack(anchor='w', padx=10, pady=5)
            
        # Actions with modern button styling
        actions = tk.Frame(dashboard_frame, bg='#f5f7fa')
        actions.pack(fill='x', padx=20, pady=15)
        
        refresh_btn = tk.Button(actions, text="🔄 Refresh Dashboard", 
                 command=self.refresh_dashboard, 
                 bg='#2196F3', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='flat', padx=15, pady=8, cursor='hand2',
                 activebackground='#1976D2', activeforeground='white')
        refresh_btn.pack(side='left', padx=5)
        
        export_btn = tk.Button(actions, text="📤 Export Website Feeds", 
                 command=self.export_web_feeds_button,
                 bg='#4CAF50', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='flat', padx=15, pady=8, cursor='hand2',
                 activebackground='#388E3C', activeforeground='white')
        export_btn.pack(side='left', padx=5)
    
    def create_rental_tab(self):
        """Create rental management tab with multiple item support"""
        # Create main container frame
        rental_frame = ttk.Frame(self.notebook)
        self.notebook.add(rental_frame, text="New Rental")
        
        # Create scrollable canvas
        canvas = tk.Canvas(rental_frame, bg='#f5f7fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(rental_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas (Windows and Linux)
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
        # Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Use scrollable_frame instead of rental_frame for all content
        rental_content = scrollable_frame
        
        # Customer selection
        customer_frame = tk.LabelFrame(rental_content, text="Customer Information", 
                                     font=("Arial", 12, "bold"))
        customer_frame.pack(fill='x', padx=10, pady=3)
        
        # Customer selection method
        selection_frame = tk.Frame(customer_frame)
        selection_frame.pack(fill='x', padx=5, pady=3)
        
        tk.Label(selection_frame, text="Select Customer:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.customer_selection_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(selection_frame, textvariable=self.customer_selection_var, 
                                         width=30, state='readonly')
        self.customer_combo.grid(row=0, column=1, padx=5, pady=5)
        self.customer_combo.bind('<<ComboboxSelected>>', self.on_customer_selected)
        
        tk.Button(selection_frame, text="New Customer", command=self.create_new_customer, 
                 bg='#3498db', fg='white').grid(row=0, column=2, padx=5, pady=5)
        
        # Customer details (auto-filled when customer selected)
        details_frame = tk.Frame(customer_frame)
        details_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.customer_name_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.customer_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(details_frame, text="Phone:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.customer_phone_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.customer_phone_var, width=20).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(details_frame, text="Address:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.customer_address_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=self.customer_address_var, width=50).grid(row=1, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
        
        tk.Label(details_frame, text="Customer Type:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.customer_type_var = tk.StringVar(value="Regular")
        type_combo = ttk.Combobox(details_frame, textvariable=self.customer_type_var, 
                                 values=["Regular", "Reseller", "VIP"], width=15, state='readonly')
        type_combo.grid(row=2, column=1, padx=5, pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_customer_type_changed)
        
        tk.Label(details_frame, text="Discount %:").grid(row=2, column=2, sticky='w', padx=5, pady=5)
        self.discount_var = tk.StringVar(value="0")
        tk.Entry(details_frame, textvariable=self.discount_var, width=10).grid(row=2, column=3, padx=5, pady=5)
        self.discount_var.trace('w', self.calculate_total)
        
        # Item selection for multiple items
        item_frame = tk.LabelFrame(rental_content, text="Add Items to Rental", 
                                 font=("Arial", 12, "bold"))
        item_frame.pack(fill='x', padx=10, pady=3)
        
        # Item selection controls
        controls_frame = tk.Frame(item_frame)
        controls_frame.pack(fill='x', padx=5, pady=3)
        
        tk.Label(controls_frame, text="Item:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.item_var = tk.StringVar()
        self.item_combo = ttk.Combobox(controls_frame, textvariable=self.item_var, width=25, state='readonly')
        self.item_combo.grid(row=0, column=1, padx=5, pady=5)
        self.item_combo.bind('<<ComboboxSelected>>', self.on_item_selected)
        
        tk.Label(controls_frame, text="Quantity:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.quantity_var = tk.StringVar()
        tk.Spinbox(controls_frame, from_=1, to=100, textvariable=self.quantity_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(controls_frame, text="Add Item", command=self.add_item_to_rental, 
                 bg='#3498db', fg='white').grid(row=0, column=4, padx=5, pady=5)
        
        # Rental items list
        list_frame = tk.Frame(item_frame)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Items listbox with scrollbar
        self.items_listbox = tk.Listbox(list_frame, height=6)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.items_listbox.yview)
        self.items_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.items_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Remove item button
        tk.Button(list_frame, text="Remove Selected", command=self.remove_selected_item, 
                 bg='#e74c3c', fg='white').pack(pady=5)
        
        # Rental period
        period_frame = tk.LabelFrame(rental_content, text="Rental Period", 
                                   font=("Arial", 12, "bold"))
        period_frame.pack(fill='x', padx=10, pady=3)
        
        tk.Label(period_frame, text="Start Date:").grid(row=0, column=0, sticky='w', padx=5, pady=3)
        self.start_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        tk.Entry(period_frame, textvariable=self.start_date_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(period_frame, text="Number of Days:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.days_var = tk.StringVar(value="1")
        tk.Spinbox(period_frame, from_=1, to=365, textvariable=self.days_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        self.days_var.trace('w', self.calculate_total)
        
        # Pricing
        pricing_frame = tk.LabelFrame(rental_content, text="Pricing (Ghana Cedis)", 
                                    font=("Arial", 12, "bold"))
        pricing_frame.pack(fill='x', padx=10, pady=3)
        
        tk.Label(pricing_frame, text="Total Amount:").grid(row=0, column=0, sticky='w', padx=5, pady=3)
        self.total_amount_var = tk.StringVar()
        tk.Label(pricing_frame, textvariable=self.total_amount_var, font=("Arial", 14, "bold"), 
                fg='green').grid(row=0, column=1, padx=5, pady=5)
        
        # Receipt and SMS options with modern styling
        options_frame = tk.LabelFrame(rental_content, text="📄 Receipt Options", 
                                     font=("Segoe UI", 11, "bold"), fg='#1a237e',
                                     bg='white', relief='flat', bd=1)
        options_frame.pack(fill='x', padx=10, pady=8)
        
        options_inner = tk.Frame(options_frame, bg='white')
        options_inner.pack(fill='x', padx=10, pady=8)
        
        self.generate_receipt_var = tk.BooleanVar(value=True)
        receipt_cb = tk.Checkbutton(options_inner, text="📋 Generate PDF Receipt", 
                      variable=self.generate_receipt_var, 
                      font=("Segoe UI", 10), bg='white',
                      activebackground='white', selectcolor='white',
                      fg='#424242')
        receipt_cb.pack(side='left', padx=15, pady=5)
        
        self.send_sms_var = tk.BooleanVar(value=False)
        sms_cb = tk.Checkbutton(options_inner, text="📱 Send Receipt via SMS", 
                      variable=self.send_sms_var, 
                      font=("Segoe UI", 10), bg='white',
                      activebackground='white', selectcolor='white',
                      fg='#424242')
        sms_cb.pack(side='left', padx=15, pady=5)
        
        # Show SMS status
        try:
            if not SMS_ENABLED:
                sms_status = tk.Label(options_inner, text="(SMS disabled - configure in sms_config.py)", 
                                    font=("Segoe UI", 8), fg='#757575', bg='white')
                sms_status.pack(side='left', padx=10)
        except:
            pass  # SMS_ENABLED might not be defined
        
        # Buttons - Fixed at bottom of scrollable area with better spacing
        button_frame = tk.Frame(rental_content, bg='#f5f7fa')
        button_frame.pack(fill='x', padx=10, pady=(15, 20))
        
        # Add separator line above buttons
        separator = tk.Frame(button_frame, height=2, bg='#e0e0e0')
        separator.pack(fill='x', pady=(0, 15))
        
        # Button container with center alignment
        btn_container = tk.Frame(button_frame, bg='#f5f7fa')
        btn_container.pack(expand=True)
        
        create_btn = tk.Button(btn_container, text="✅ Create Rental", command=self.create_rental, 
                 bg='#4CAF50', fg='white', font=("Segoe UI", 12, "bold"),
                 relief='flat', padx=25, pady=12, cursor='hand2',
                 activebackground='#388E3C', activeforeground='white')
        create_btn.pack(side='left', padx=8)
        
        clear_btn = tk.Button(btn_container, text="🗑️ Clear Form", command=self.clear_rental_form, 
                 bg='#f44336', fg='white', font=("Segoe UI", 12, "bold"),
                 relief='flat', padx=25, pady=12, cursor='hand2',
                 activebackground='#d32f2f', activeforeground='white')
        clear_btn.pack(side='left', padx=8)
        
        # Load items and customers
        self.load_items()
        self.load_customers()
    
    def load_customers(self):
        """Load customers into the combo box"""
        try:
            db = SessionLocal()
            customers = db.query(Customer).all()
            customer_names = [f"{customer.name} ({customer.customer_type})" for customer in customers]
            self.customer_combo['values'] = customer_names
        except Exception as e:
            print(f"Customer loading error: {e}")
            # Don't show error message for missing combo box
        finally:
            if 'db' in locals():
                db.close()
    
    def on_customer_selected(self, event):
        """Handle customer selection"""
        selected = self.customer_combo.get()
        if selected:
            customer_name = selected.split(' (')[0]
            db = SessionLocal()
            try:
                customer = db.query(Customer).filter(Customer.name == customer_name).first()
                if customer:
                    self.customer_name_var.set(customer.name)
                    self.customer_phone_var.set(customer.phone or "")
                    self.customer_address_var.set(customer.address or "")
                    self.customer_type_var.set(customer.customer_type)
                    self.discount_var.set(str(customer.discount_percentage))
                    self.calculate_total()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load customer details: {e}")
            finally:
                db.close()
    
    def on_customer_type_changed(self, event):
        """Handle customer type change"""
        customer_type = self.customer_type_var.get()
        if customer_type == "Reseller":
            self.discount_var.set("10")  # Default 10% discount for resellers
        elif customer_type == "VIP":
            self.discount_var.set("15")  # Default 15% discount for VIP
        else:
            self.discount_var.set("0")   # No discount for regular customers
        self.calculate_total()
    
    def create_new_customer(self):
        """Create a new customer"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Customer Name:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Phone:").pack(pady=5)
        phone_var = tk.StringVar()
        tk.Entry(dialog, textvariable=phone_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Email:").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(dialog, textvariable=email_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Address:").pack(pady=5)
        address_var = tk.StringVar()
        tk.Entry(dialog, textvariable=address_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Customer Type:").pack(pady=5)
        type_var = tk.StringVar(value="Regular")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["Regular", "Reseller", "VIP"], width=37, state='readonly')
        type_combo.pack(pady=5)
        
        tk.Label(dialog, text="Discount Percentage:").pack(pady=5)
        discount_var = tk.StringVar(value="0")
        tk.Entry(dialog, textvariable=discount_var, width=40).pack(pady=5)
        
        tk.Label(dialog, text="Notes:").pack(pady=5)
        notes_var = tk.StringVar()
        tk.Entry(dialog, textvariable=notes_var, width=40).pack(pady=5)
        
        def save_customer():
            try:
                db = SessionLocal()
                customer = Customer(
                    name=name_var.get(),
                    phone=phone_var.get(),
                    email=email_var.get(),
                    address=address_var.get(),
                    customer_type=type_var.get(),
                    discount_percentage=float(discount_var.get()),
                    notes=notes_var.get()
                )
                db.add(customer)
                db.commit()
                messagebox.showinfo("Success", "Customer added successfully")
                dialog.destroy()
                self.load_customers()
                self.refresh_customers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {e}")
            finally:
                db.close()
        
        tk.Button(dialog, text="Save Customer", command=save_customer).pack(pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def create_inventory_tab(self):
        """Create inventory management tab"""
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")
        
        # Inventory tree
        columns = ('ID', 'Name', 'Description', 'Total Qty', 'Available Qty', 'Daily Rate (GHS)')
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=120)
        
        # Scrollbar
        inventory_scrollbar = ttk.Scrollbar(inventory_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=inventory_scrollbar.set)
        
        self.inventory_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        inventory_scrollbar.pack(side='right', fill='y')
        
        # Search and filter frame
        search_frame = tk.Frame(inventory_frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search Items:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_inventory)
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Clear Search", command=self.clear_search).pack(side='left', padx=5)
        
        # Buttons
        button_frame = tk.Frame(inventory_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh Inventory", command=self.refresh_inventory).pack(side='left', padx=5)
        tk.Button(button_frame, text="Add New Item", command=self.add_new_item).pack(side='left', padx=5)
        tk.Button(button_frame, text="Edit Selected Item", command=self.edit_selected_item, 
                 bg='#f39c12', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Selected Item", command=self.delete_selected_item, 
                 bg='#e74c3c', fg='white').pack(side='left', padx=5)
        
        # Load inventory
        self.refresh_inventory()
    
    def create_customers_tab(self):
        """Create customers management tab"""
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="Customers")
        
        # Customers tree
        columns = ('ID', 'Name', 'Type', 'Phone', 'Email', 'Address', 'Discount %', 'Created')
        self.customers_tree = ttk.Treeview(customers_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=150)
        
        # Scrollbar
        customers_scrollbar = ttk.Scrollbar(customers_frame, orient='vertical', command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=customers_scrollbar.set)
        
        self.customers_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        customers_scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(customers_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh Customers", command=self.refresh_customers).pack(side='left', padx=5)
        tk.Button(button_frame, text="Add New Customer", command=self.create_new_customer).pack(side='left', padx=5)
        tk.Button(button_frame, text="Edit Selected Customer", command=self.edit_selected_customer, 
                 bg='#f39c12', fg='white').pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Selected Customer", command=self.delete_selected_customer, 
                 bg='#e74c3c', fg='white').pack(side='left', padx=5)
        
        # Load customers
        self.refresh_customers()
    
    def create_rentals_tab(self):
        """Create active rentals management tab"""
        rentals_frame = ttk.Frame(self.notebook)
        self.notebook.add(rentals_frame, text="Active Rentals")
        
        # Rentals title
        tk.Label(rentals_frame, text="Active Rentals Management", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Rentals tree
        columns = ('ID', 'Customer', 'Items', 'Start Date', 'Return Date', 'Amount (GHS)')
        self.rentals_tree = ttk.Treeview(rentals_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=120)
        
        # Scrollbar
        rentals_scrollbar = ttk.Scrollbar(rentals_frame, orient='vertical', command=self.rentals_tree.yview)
        self.rentals_tree.configure(yscrollcommand=rentals_scrollbar.set)
        
        self.rentals_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        rentals_scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(rentals_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh Rentals", command=self.refresh_rentals).pack(side='left', padx=5)
        tk.Button(button_frame, text="Mark as Returned", command=self.mark_as_returned, 
                 bg='#27ae60', fg='white').pack(side='left', padx=5)
        
        # Load rentals
        self.refresh_rentals()
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Active rentals
        tk.Label(reports_frame, text="Active Rentals", font=("Arial", 14, "bold")).pack(pady=10)
        
        columns = ('ID', 'Customer', 'Items', 'Start Date', 'Return Date', 'Amount (GHS)')
        self.rentals_tree = ttk.Treeview(reports_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.rentals_tree.heading(col, text=col)
            self.rentals_tree.column(col, width=120)
        
        # Scrollbar
        rentals_scrollbar = ttk.Scrollbar(reports_frame, orient='vertical', command=self.rentals_tree.yview)
        self.rentals_tree.configure(yscrollcommand=rentals_scrollbar.set)
        
        self.rentals_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        rentals_scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(reports_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh Rentals", command=self.refresh_rentals).pack(side='left', padx=5)
        tk.Button(button_frame, text="Mark as Returned", command=self.mark_as_returned).pack(side='left', padx=5)
        
        # Load rentals
        self.refresh_rentals()
    
    def create_history_tab(self):
        """Create rental history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Rental History")
        
        # History title
        tk.Label(history_frame, text="Rental History - Past Rentals", font=("Arial", 14, "bold")).pack(pady=10)
        
        # History tree
        columns = ('ID', 'Customer', 'Items', 'Start Date', 'Return Date', 'Amount (GHS)', 'Status')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=120)
        
        # Scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        history_scrollbar.pack(side='right', fill='y')
        
        # Buttons
        button_frame = tk.Frame(history_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh History", command=self.refresh_history).pack(side='left', padx=5)
        tk.Button(button_frame, text="Export History", command=self.export_history).pack(side='left', padx=5)
        
        # Load history
        self.refresh_history()
    
    def load_items(self):
        """Load items into the combo box"""
        db = SessionLocal()
        try:
            items = db.query(Item).all()
            item_names = [f"{item.name} (Available: {item.available_quantity})" for item in items]
            self.item_combo['values'] = item_names
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load items: {e}")
        finally:
            db.close()
    
    def on_item_selected(self, event):
        """Handle item selection"""
        selected = self.item_combo.get()
        if selected:
            item_name = selected.split(' (Available:')[0]
            db = SessionLocal()
            try:
                item = db.query(Item).filter(Item.name == item_name).first()
                if item:
                    self.current_item = item
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load item details: {e}")
            finally:
                db.close()
    
    def add_item_to_rental(self):
        """Add item to rental list"""
        if not hasattr(self, 'current_item') or not self.current_item:
            messagebox.showwarning("Warning", "Please select an item first")
            return
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0")
                return
            
            if self.current_item.available_quantity < quantity:
                messagebox.showerror("Error", f"Not enough items available. Only {self.current_item.available_quantity} available")
                return
            
            # Check if item already in rental
            for rental_item in self.rental_items:
                if rental_item['item'].id == self.current_item.id:
                    messagebox.showwarning("Warning", "This item is already in the rental. Please remove it first to change quantity.")
                    return
            
            # Add to rental items
            rental_item = {
                'item': self.current_item,
                'quantity': quantity
            }
            self.rental_items.append(rental_item)
            
            # Update listbox
            self.update_rental_items_display()
            self.calculate_total()
            
            # Clear selection
            self.item_var.set("")
            self.quantity_var.set("1")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
    
    def remove_selected_item(self):
        """Remove selected item from rental"""
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        index = selection[0]
        if 0 <= index < len(self.rental_items):
            del self.rental_items[index]
            self.update_rental_items_display()
            self.calculate_total()
    
    def update_rental_items_display(self):
        """Update the rental items listbox display"""
        self.items_listbox.delete(0, tk.END)
        for rental_item in self.rental_items:
            item = rental_item['item']
            quantity = rental_item['quantity']
            total_price = item.daily_rate * quantity
            display_text = f"{item.name} x{quantity} @ GHS {item.daily_rate:.2f} = GHS {total_price:.2f}"
            self.items_listbox.insert(tk.END, display_text)
    
    def calculate_total(self, *args):
        """Calculate total rental amount with customer discount"""
        try:
            days = int(self.days_var.get()) if self.days_var.get() else 0
            discount = float(self.discount_var.get()) if self.discount_var.get() else 0
            total = 0
            
            for rental_item in self.rental_items:
                item = rental_item['item']
                quantity = rental_item['quantity']
                total += item.daily_rate * quantity * days
            
            # Apply discount
            discount_amount = total * (discount / 100)
            final_total = total - discount_amount
            
            # Display with discount breakdown
            if discount > 0:
                self.total_amount_var.set(f"GHS {final_total:.2f} (Discount: {discount}% = GHS {discount_amount:.2f})")
            else:
                self.total_amount_var.set(f"GHS {final_total:.2f}")
        except:
            self.total_amount_var.set("GHS 0.00")
    
    def create_rental(self):
        """Create a new rental with multiple items"""
        try:
            # Validate inputs
            if not self.customer_name_var.get():
                messagebox.showerror("Error", "Please enter customer name")
                return
            
            if not self.rental_items:
                messagebox.showerror("Error", "Please add at least one item to the rental")
                return
            
            days = int(self.days_var.get())
            if days <= 0:
                messagebox.showerror("Error", "Number of days must be greater than 0")
                return
            
            # Get or create customer
            db = SessionLocal()
            try:
                customer = db.query(Customer).filter(Customer.name == self.customer_name_var.get()).first()
                if not customer:
                    customer = Customer(
                        name=self.customer_name_var.get(),
                        phone=self.customer_phone_var.get(),
                        address=self.customer_address_var.get(),
                        customer_type=self.customer_type_var.get(),
                        discount_percentage=float(self.discount_var.get())
                    )
                    db.add(customer)
                    db.flush()
                else:
                    # Update existing customer if details changed
                    customer.phone = self.customer_phone_var.get()
                    customer.address = self.customer_address_var.get()
                    customer.customer_type = self.customer_type_var.get()
                    customer.discount_percentage = float(self.discount_var.get())
                
                # Create rental for each item
                total_amount = 0
                discount = float(self.discount_var.get())
                start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
                return_date = start_date + timedelta(days=days)
                
                for rental_item in self.rental_items:
                    item = rental_item['item']
                    quantity = rental_item['quantity']
                    
                    # Check availability again
                    if item.available_quantity < quantity:
                        messagebox.showerror("Error", f"Not enough {item.name} available. Only {item.available_quantity} available")
                        return
                    
                    # Calculate item total with discount
                    item_total = item.daily_rate * quantity * days
                    discount_amount = item_total * (discount / 100)
                    final_item_total = item_total - discount_amount
                    
                    # Create rental record
                    rental = Rental(
                        customer_id=customer.id,
                        item_id=item.id,
                        quantity=quantity,
                        rental_date=start_date,
                        return_date=return_date,
                        daily_rate=item.daily_rate,
                        total_amount=final_item_total
                    )
                    
                    db.add(rental)
                    
                    # Update available quantity
                    item.available_quantity -= quantity
                    total_amount += rental.total_amount
                
                db.commit()
                
                # Get the first rental ID for receipt (they all share the same customer/date)
                first_rental = db.query(Rental).filter(
                    Rental.customer_id == customer.id,
                    Rental.rental_date == start_date
                ).first()
                
                rental_id = first_rental.id if first_rental else "N/A"
                
                # Generate receipt and send SMS if requested
                receipt_path = None
                sms_sent = False
                sms_message = ""
                
                if RECEIPT_AVAILABLE and self.generate_receipt_var.get():
                    try:
                        receipt_path = self.generate_receipt(
                            rental_id=rental_id,
                            customer=customer,
                            rental_items=self.rental_items,
                            start_date=start_date,
                            return_date=return_date,
                            days=days,
                            discount=discount,
                            total_amount=total_amount
                        )
                    except Exception as e:
                        print(f"Receipt generation error: {e}")
                        receipt_path = None
                
                if RECEIPT_AVAILABLE and self.send_sms_var.get() and customer.phone:
                    if SMS_ENABLED:
                        try:
                            sms_result = self.send_receipt_sms(
                                customer.phone,
                                customer.name,
                                rental_id,
                                total_amount,
                                return_date.strftime('%Y-%m-%d'),
                                receipt_path
                            )
                            sms_sent = sms_result.get('success', False)
                            sms_message = sms_result.get('message', '')
                        except Exception as e:
                            print(f"SMS sending error: {e}")
                            sms_message = f"SMS error: {str(e)}"
                    else:
                        sms_message = "SMS is disabled. Configure SMS gateway in sms_config.py"
                
                # Success message
                success_msg = f"Rental created successfully!\nTotal Amount: GHS {total_amount:.2f}"
                if receipt_path:
                    success_msg += f"\n\nReceipt saved: {receipt_path}"
                if sms_sent:
                    success_msg += f"\n\nSMS sent successfully!"
                elif self.send_sms_var.get() and sms_message:
                    success_msg += f"\n\nSMS: {sms_message}"
                
                messagebox.showinfo("Success", success_msg)
                self.clear_rental_form()
                self.refresh_inventory()
                self.refresh_rentals()
                self.refresh_history()
                self.refresh_dashboard()
                self.export_web_json_feeds()
                
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to create rental: {e}")
            finally:
                db.close()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for days")
    
    def clear_rental_form(self):
        """Clear the rental form"""
        self.customer_selection_var.set("")
        self.customer_name_var.set("")
        self.customer_phone_var.set("")
        self.customer_address_var.set("")
        self.customer_type_var.set("Regular")
        self.discount_var.set("0")
        self.item_var.set("")
        self.quantity_var.set("1")
        self.start_date_var.set(date.today().strftime('%Y-%m-%d'))
        self.days_var.set("1")
        self.total_amount_var.set("GHS 0.00")
        self.rental_items = []
        self.update_rental_items_display()
        # Reset receipt options
        if hasattr(self, 'generate_receipt_var'):
            self.generate_receipt_var.set(True)
        if hasattr(self, 'send_sms_var'):
            self.send_sms_var.set(False)
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            db = SessionLocal()
            
            # Get total items
            total_items = db.query(Item).count()
            
            # Get total customers
            total_customers = db.query(Customer).count()
            
            # Get active rentals
            active_rentals = db.query(Rental).filter(Rental.is_returned == False).count()
            
            # Get total revenue
            total_revenue = db.query(Rental).filter(Rental.is_returned == True).with_entities(
                func.sum(Rental.total_amount)
            ).scalar() or 0
            
            # Update dashboard labels if they exist
            if hasattr(self, 'total_items_label'):
                self.total_items_label.config(text=f"Total Items: {total_items}")
            if hasattr(self, 'total_customers_label'):
                self.total_customers_label.config(text=f"Total Customers: {total_customers}")
            if hasattr(self, 'active_rentals_label'):
                self.active_rentals_label.config(text=f"Active Rentals: {active_rentals}")
            if hasattr(self, 'total_revenue_label'):
                self.total_revenue_label.config(text=f"Total Revenue: GHS {total_revenue:.2f}")
                
        except Exception as e:
            print(f"Dashboard refresh error: {e}")
        finally:
            db.close()
    
    def refresh_inventory(self):
        """Refresh inventory display"""
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        db = SessionLocal()
        try:
            items = db.query(Item).all()
            for item in items:
                self.inventory_tree.insert('', 'end', values=(
                    item.id,
                    item.name,
                    item.description,
                    item.total_quantity,
                    item.available_quantity,
                    f"GHS {item.daily_rate:.2f}"
                ))
        except Exception as e:
            print(f"Inventory refresh error: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    def refresh_customers(self):
        """Refresh customers display"""
        try:
            # Clear existing customers
            for customer in self.customers_tree.get_children():
                self.customers_tree.delete(customer)
            
            db = SessionLocal()
            customers = db.query(Customer).all()
            for customer in customers:
                self.customers_tree.insert('', 'end', values=(
                    customer.id,
                    customer.name,
                    customer.customer_type,
                    customer.phone or "",
                    customer.email or "",
                    customer.address or "",
                    f"{customer.discount_percentage}%",
                    customer.created_at.strftime('%Y-%m-%d')
                ))
        except Exception as e:
            print(f"Customer refresh error: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    def refresh_rentals(self):
        """Refresh rentals display"""
        # Clear existing rentals
        for rental in self.rentals_tree.get_children():
            self.rentals_tree.delete(rental)
        
        db = SessionLocal()
        try:
            rentals = db.query(Rental).filter(Rental.is_returned == False).all()
            # Group rentals by customer and date
            rental_groups = {}
            for rental in rentals:
                key = f"{rental.customer.name}_{rental.rental_date}_{rental.return_date}"
                if key not in rental_groups:
                    rental_groups[key] = {
                        'customer': rental.customer.name,
                        'start_date': rental.rental_date,
                        'return_date': rental.return_date,
                        'items': [],
                        'total_amount': 0
                    }
                rental_groups[key]['items'].append(f"{rental.item.name} x{rental.quantity}")
                rental_groups[key]['total_amount'] += rental.total_amount
            
            for group in rental_groups.values():
                items_str = ", ".join(group['items'])
                self.rentals_tree.insert('', 'end', values=(
                    "",  # No single ID for grouped rentals
                    group['customer'],
                    items_str,
                    group['start_date'].strftime('%Y-%m-%d'),
                    group['return_date'].strftime('%Y-%m-%d'),
                    f"GHS {group['total_amount']:.2f}"
                ))
        except Exception as e:
            print(f"Rentals refresh error: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    def mark_as_returned(self):
        """Mark selected rental as returned"""
        selection = self.rentals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a rental to mark as returned")
            return
        
        # For grouped rentals, we need to find all related rentals
        customer_name = self.rentals_tree.item(selection[0])['values'][1]
        start_date = self.rentals_tree.item(selection[0])['values'][3]
        
        db = SessionLocal()
        try:
            # Find all rentals for this customer and date
            rentals = db.query(Rental).join(Customer).filter(
                Customer.name == customer_name,
                Rental.rental_date == datetime.strptime(start_date, '%Y-%m-%d').date(),
                Rental.is_returned == False
            ).all()
            
            for rental in rentals:
                rental.is_returned = True
                # Return items to available quantity
                rental.item.available_quantity += rental.quantity
            
            db.commit()
            messagebox.showinfo("Success", "Rental marked as returned")
            self.refresh_rentals()
            self.refresh_inventory()
            self.refresh_history()  # Refresh history to show returned rental
            self.export_web_json_feeds()
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Failed to mark rental as returned: {e}")
        finally:
            db.close()
    
    def add_new_item(self):
        """Add a new item to inventory"""
        # Create a simple dialog for adding new items
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Item")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Item Name:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var, width=30).pack(pady=5)
        
        tk.Label(dialog, text="Description:").pack(pady=5)
        desc_var = tk.StringVar()
        tk.Entry(dialog, textvariable=desc_var, width=30).pack(pady=5)
        
        tk.Label(dialog, text="Total Quantity:").pack(pady=5)
        qty_var = tk.StringVar(value="0")
        tk.Spinbox(dialog, from_=0, to=1000, textvariable=qty_var, width=10).pack(pady=5)
        
        tk.Label(dialog, text="Daily Rate (GHS):").pack(pady=5)
        rate_var = tk.StringVar(value="0.00")
        tk.Entry(dialog, textvariable=rate_var, width=15).pack(pady=5)
        
        def save_item():
            try:
                db = SessionLocal()
                item = Item(
                    name=name_var.get(),
                    description=desc_var.get(),
                    total_quantity=int(qty_var.get()),
                    available_quantity=int(qty_var.get()),
                    daily_rate=float(rate_var.get())
                )
                db.add(item)
                db.commit()
                messagebox.showinfo("Success", "Item added successfully")
                dialog.destroy()
                self.refresh_inventory()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add item: {e}")
            finally:
                db.close()
        
        tk.Button(dialog, text="Save", command=save_item).pack(pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def filter_inventory(self, *args):
        """Filter inventory based on search term"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        db = SessionLocal()
        try:
            items = db.query(Item).all()
            for item in items:
                # Check if search term matches item name or description
                if (search_term == "" or 
                    search_term in item.name.lower() or 
                    search_term in (item.description or "").lower()):
                    
                    self.inventory_tree.insert('', 'end', values=(
                        item.id,
                        item.name,
                        item.description,
                        item.total_quantity,
                        item.available_quantity,
                        f"GHS {item.daily_rate:.2f}"
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter inventory: {e}")
        finally:
            db.close()
    
    def clear_search(self):
        """Clear search and show all items"""
        self.search_var.set("")
        self.refresh_inventory()
    
    def edit_selected_item(self):
        """Edit the selected item"""
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        
        # Get selected item ID
        item_id = self.inventory_tree.item(selection[0])['values'][0]
        
        db = SessionLocal()
        try:
            item = db.query(Item).filter(Item.id == item_id).first()
            if not item:
                messagebox.showerror("Error", "Item not found")
                return
            
            # Create edit dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Item")
            dialog.geometry("400x300")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Form fields with current values
            tk.Label(dialog, text="Item Name:").pack(pady=5)
            name_var = tk.StringVar(value=item.name)
            tk.Entry(dialog, textvariable=name_var, width=30).pack(pady=5)
            
            tk.Label(dialog, text="Description:").pack(pady=5)
            desc_var = tk.StringVar(value=item.description or "")
            tk.Entry(dialog, textvariable=desc_var, width=30).pack(pady=5)
            
            tk.Label(dialog, text="Total Quantity:").pack(pady=5)
            qty_var = tk.StringVar(value=str(item.total_quantity))
            tk.Spinbox(dialog, from_=0, to=1000, textvariable=qty_var, width=10).pack(pady=5)
            
            tk.Label(dialog, text="Available Quantity:").pack(pady=5)
            avail_var = tk.StringVar(value=str(item.available_quantity))
            tk.Spinbox(dialog, from_=0, to=1000, textvariable=avail_var, width=10).pack(pady=5)
            
            tk.Label(dialog, text="Daily Rate (GHS):").pack(pady=5)
            rate_var = tk.StringVar(value=str(item.daily_rate))
            tk.Entry(dialog, textvariable=rate_var, width=15).pack(pady=5)
            
            def save_changes():
                try:
                    # Update item
                    item.name = name_var.get()
                    item.description = desc_var.get()
                    item.total_quantity = int(qty_var.get())
                    item.available_quantity = int(avail_var.get())
                    item.daily_rate = float(rate_var.get())
                    
                    db.commit()
                    messagebox.showinfo("Success", "Item updated successfully")
                    dialog.destroy()
                    self.refresh_inventory()
                    self.load_items()  # Refresh combo box
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update item: {e}")
            
            tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=10)
            tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load item: {e}")
        finally:
            db.close()
    
    def delete_selected_item(self):
        """Delete the selected item"""
        selection = self.inventory_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        # Get selected item details
        item_id = self.inventory_tree.item(selection[0])['values'][0]
        item_name = self.inventory_tree.item(selection[0])['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{item_name}'?\n\nThis will also delete all related rental records!")
        
        if confirm:
            db = SessionLocal()
            try:
                # Check if item has active rentals
                active_rentals = db.query(Rental).filter(
                    Rental.item_id == item_id,
                    Rental.is_returned == False
                ).count()
                
                if active_rentals > 0:
                    messagebox.showerror("Error", f"Cannot delete item. It has {active_rentals} active rental(s).\nPlease mark all rentals as returned first.")
                    return
                
                # Delete all rentals for this item first
                db.query(Rental).filter(Rental.item_id == item_id).delete()
                
                # Delete the item
                db.query(Item).filter(Item.id == item_id).delete()
                
                db.commit()
                messagebox.showinfo("Success", f"Item '{item_name}' deleted successfully")
                self.refresh_inventory()
                self.load_items()  # Refresh combo box
                
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete item: {e}")
            finally:
                db.close()
    
    def refresh_history(self):
        """Refresh rental history display"""
        # Clear existing history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        db = SessionLocal()
        try:
            # Get all rentals (both active and returned)
            rentals = db.query(Rental).all()
            
            # Group rentals by customer and date
            rental_groups = {}
            for rental in rentals:
                key = f"{rental.customer.name}_{rental.rental_date}_{rental.return_date}"
                if key not in rental_groups:
                    rental_groups[key] = {
                        'id': rental.id,
                        'customer': rental.customer.name,
                        'start_date': rental.rental_date,
                        'return_date': rental.return_date,
                        'items': [],
                        'total_amount': 0,
                        'is_returned': rental.is_returned
                    }
                rental_groups[key]['items'].append(f"{rental.item.name} x{rental.quantity}")
                rental_groups[key]['total_amount'] += rental.total_amount
            
            # Sort by start date (newest first)
            sorted_groups = sorted(rental_groups.values(), key=lambda x: x['start_date'], reverse=True)
            
            for group in sorted_groups:
                items_str = ", ".join(group['items'])
                status = "Returned" if group['is_returned'] else "Active"
                self.history_tree.insert('', 'end', values=(
                    group['id'],
                    group['customer'],
                    items_str,
                    group['start_date'].strftime('%Y-%m-%d'),
                    group['return_date'].strftime('%Y-%m-%d'),
                    f"GHS {group['total_amount']:.2f}",
                    status
                ))
        except Exception as e:
            print(f"History refresh error: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    def export_history(self):
        """Export rental history to a text file"""
        try:
            from tkinter import filedialog
            
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Rental History"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("ALYVON Rental Management System - Rental History\n")
                    f.write("=" * 60 + "\n\n")
                    
                    # Get all rental data
                    db = SessionLocal()
                    try:
                        rentals = db.query(Rental).all()
                        
                        # Group rentals
                        rental_groups = {}
                        for rental in rentals:
                            key = f"{rental.customer.name}_{rental.rental_date}_{rental.return_date}"
                            if key not in rental_groups:
                                rental_groups[key] = {
                                    'customer': rental.customer.name,
                                    'start_date': rental.rental_date,
                                    'return_date': rental.return_date,
                                    'items': [],
                                    'total_amount': 0,
                                    'is_returned': rental.is_returned
                                }
                            rental_groups[key]['items'].append(f"{rental.item.name} x{rental.quantity}")
                            rental_groups[key]['total_amount'] += rental.total_amount
                        
                        # Sort by start date
                        sorted_groups = sorted(rental_groups.values(), key=lambda x: x['start_date'], reverse=True)
                        
                        for i, group in enumerate(sorted_groups, 1):
                            f.write(f"Rental #{i}\n")
                            f.write(f"Customer: {group['customer']}\n")
                            f.write(f"Items: {', '.join(group['items'])}\n")
                            f.write(f"Start Date: {group['start_date'].strftime('%Y-%m-%d')}\n")
                            f.write(f"Return Date: {group['return_date'].strftime('%Y-%m-%d')}\n")
                            f.write(f"Total Amount: GHS {group['total_amount']:.2f}\n")
                            f.write(f"Status: {'Returned' if group['is_returned'] else 'Active'}\n")
                            f.write("-" * 40 + "\n\n")
                        
                        f.write(f"Total Rentals: {len(sorted_groups)}\n")
                        f.write(f"Total Revenue: GHS {sum(g['total_amount'] for g in sorted_groups):.2f}\n")
                        
                    except Exception as e:
                        f.write(f"Error loading data: {e}\n")
                    finally:
                        db.close()
                
                messagebox.showinfo("Success", f"Rental history exported to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export history: {e}")
    
    def edit_selected_customer(self):
        """Edit the selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return
        
        # Get selected customer ID
        customer_id = self.customers_tree.item(selection[0])['values'][0]
        
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                messagebox.showerror("Error", "Customer not found")
                return
            
            # Create edit dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Customer")
            dialog.geometry("500x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Form fields with current values
            tk.Label(dialog, text="Customer Name:").pack(pady=5)
            name_var = tk.StringVar(value=customer.name)
            tk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)
            
            tk.Label(dialog, text="Phone:").pack(pady=5)
            phone_var = tk.StringVar(value=customer.phone or "")
            tk.Entry(dialog, textvariable=phone_var, width=40).pack(pady=5)
            
            tk.Label(dialog, text="Email:").pack(pady=5)
            email_var = tk.StringVar(value=customer.email or "")
            tk.Entry(dialog, textvariable=email_var, width=40).pack(pady=5)
            
            tk.Label(dialog, text="Address:").pack(pady=5)
            address_var = tk.StringVar(value=customer.address or "")
            tk.Entry(dialog, textvariable=address_var, width=40).pack(pady=5)
            
            tk.Label(dialog, text="Customer Type:").pack(pady=5)
            type_var = tk.StringVar(value=customer.customer_type)
            type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                     values=["Regular", "Reseller", "VIP"], width=37, state='readonly')
            type_combo.pack(pady=5)
            
            tk.Label(dialog, text="Discount Percentage:").pack(pady=5)
            discount_var = tk.StringVar(value=str(customer.discount_percentage))
            tk.Entry(dialog, textvariable=discount_var, width=40).pack(pady=5)
            
            tk.Label(dialog, text="Notes:").pack(pady=5)
            notes_var = tk.StringVar(value=customer.notes or "")
            tk.Entry(dialog, textvariable=notes_var, width=40).pack(pady=5)
            
            def save_changes():
                try:
                    # Update customer
                    customer.name = name_var.get()
                    customer.phone = phone_var.get()
                    customer.email = email_var.get()
                    customer.address = address_var.get()
                    customer.customer_type = type_var.get()
                    customer.discount_percentage = float(discount_var.get())
                    customer.notes = notes_var.get()
                    
                    db.commit()
                    messagebox.showinfo("Success", "Customer updated successfully")
                    dialog.destroy()
                    self.refresh_customers()
                    self.load_customers()  # Refresh combo box
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update customer: {e}")
            
            tk.Button(dialog, text="Save Changes", command=save_changes).pack(pady=10)
            tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customer: {e}")
        finally:
            db.close()
    
    def delete_selected_customer(self):
        """Delete the selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return
        
        # Get selected customer details
        customer_id = self.customers_tree.item(selection[0])['values'][0]
        customer_name = self.customers_tree.item(selection[0])['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete customer '{customer_name}'?\n\nThis will also delete all related rental records!")
        
        if confirm:
            db = SessionLocal()
            try:
                # Check if customer has active rentals
                active_rentals = db.query(Rental).filter(
                    Rental.customer_id == customer_id,
                    Rental.is_returned == False
                ).count()
                
                if active_rentals > 0:
                    messagebox.showerror("Error", f"Cannot delete customer. They have {active_rentals} active rental(s).\nPlease mark all rentals as returned first.")
                    return
                
                # Delete all rentals for this customer first
                db.query(Rental).filter(Rental.customer_id == customer_id).delete()
                
                # Delete the customer
                db.query(Customer).filter(Customer.id == customer_id).delete()
                
                db.commit()
                messagebox.showinfo("Success", f"Customer '{customer_name}' deleted successfully")
                self.refresh_customers()
                self.load_customers()  # Refresh combo box
                
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to delete customer: {e}")
            finally:
                db.close()

    def generate_receipt(self, rental_id, customer, rental_items, start_date, return_date, days, discount, total_amount):
        """Generate PDF receipt for a rental"""
        if not RECEIPT_AVAILABLE:
            return None
        
        try:
            generator = ReceiptGenerator(
                company_name=COMPANY_NAME,
                company_phone=COMPANY_PHONE,
                company_email=COMPANY_EMAIL,
                company_address=COMPANY_ADDRESS
            )
            
            # Prepare items data
            items_data = []
            subtotal = 0
            for rental_item in rental_items:
                item = rental_item['item']
                quantity = rental_item['quantity']
                item_subtotal = item.daily_rate * quantity * days
                subtotal += item_subtotal
                
                items_data.append({
                    'name': item.name,
                    'quantity': quantity,
                    'daily_rate': item.daily_rate,
                    'days': days,
                    'subtotal': item_subtotal
                })
            
            discount_amount = subtotal * (discount / 100)
            
            rental_data = {
                'rental_id': rental_id,
                'customer_name': customer.name,
                'customer_phone': customer.phone or '',
                'customer_address': customer.address or '',
                'rental_date': start_date.strftime('%B %d, %Y') if isinstance(start_date, date) else str(start_date),
                'return_date': return_date.strftime('%B %d, %Y') if isinstance(return_date, date) else str(return_date),
                'items': items_data,
                'subtotal': subtotal,
                'discount_percent': discount,
                'discount_amount': discount_amount,
                'total_amount': total_amount,
                'currency': 'GHS'
            }
            
            receipt_path = generator.generate_receipt(rental_data)
            return receipt_path
        except Exception as e:
            print(f"Receipt generation error: {e}")
            return None
    
    def send_receipt_sms(self, phone_number, customer_name, rental_id, total_amount, return_date, receipt_path=None):
        """Send receipt notification via SMS"""
        if not RECEIPT_AVAILABLE:
            return {'success': False, 'message': 'SMS module not available'}
        
        try:
            # Configure SMS sender
            sms_config = get_sms_config()
            sender = SMSSender()
            sender.gateway = sms_config['gateway']
            sender.api_key = sms_config['api_key']
            sender.api_secret = sms_config['api_secret']
            sender.sender_id = sms_config['sender_id']
            
            if sender.gateway == 'disabled':
                return {'success': False, 'message': 'SMS is disabled. Configure SMS gateway in sms_config.py'}
            
            # Send SMS
            result = sender.send_receipt_notification(
                phone_number=phone_number,
                customer_name=customer_name,
                rental_id=str(rental_id),
                total_amount=float(total_amount),
                return_date=return_date,
                currency='GHS'
            )
            
            return result
        except Exception as e:
            return {'success': False, 'message': f'Error sending SMS: {str(e)}'}

    def export_web_feeds_button(self):
        """Export JSON feeds and copy logo for the website (dashboard button)."""
        try:
            export_web_json_feeds()
            messagebox.showinfo("Export Complete", "Website feeds exported to web/data/ and logo copied.")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export web feeds: {e}")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = RentalManagerApp(root)
    root.mainloop()

# ---- Web JSON feeds (read-only site support) ----
def ensure_web_paths():
    try:
        os.makedirs(os.path.join('web','data'), exist_ok=True)
    except Exception:
        pass

def build_active_rentals_payload(db):
    rentals = db.query(Rental).filter(Rental.is_returned == False).all()
    groups = {}
    for r in rentals:
        key = f"{r.customer.name}_{r.rental_date}_{r.return_date}"
        if key not in groups:
            groups[key] = {
                'customer': r.customer.name,
                'start_date': r.rental_date.isoformat() if r.rental_date else None,
                'return_date': r.return_date.isoformat() if r.return_date else None,
                'items': [],
                'total_amount': 0
            }
        groups[key]['items'].append(f"{r.item.name} x{r.quantity}")
        groups[key]['total_amount'] += float(r.total_amount or 0)
    return list(groups.values())

def build_history_payload(db):
    rentals = db.query(Rental).all()
    groups = {}
    for r in rentals:
        key = f"{r.customer.name}_{r.rental_date}_{r.return_date}"
        if key not in groups:
            groups[key] = {
                'customer': r.customer.name,
                'start_date': r.rental_date.isoformat() if r.rental_date else None,
                'return_date': r.return_date.isoformat() if r.return_date else None,
                'items': [],
                'total_amount': 0,
                'is_returned': bool(r.is_returned)
            }
        groups[key]['items'].append(f"{r.item.name} x{r.quantity}")
        groups[key]['total_amount'] += float(r.total_amount or 0)
        # If any rental in the group is active, keep as active; only mark returned if all are returned
        groups[key]['is_returned'] = groups[key]['is_returned'] and bool(r.is_returned)
    return list(groups.values())

def export_web_json_feeds():
    try:
        ensure_web_paths()
        db = SessionLocal()
        active_payload = build_active_rentals_payload(db)
        history_payload = build_history_payload(db)
        with open(os.path.join('web','data','active_rentals.json'), 'w', encoding='utf-8') as f:
            json.dump(active_payload, f, ensure_ascii=False)
        with open(os.path.join('web','data','rental_history.json'), 'w', encoding='utf-8') as f:
            json.dump(history_payload, f, ensure_ascii=False)
        # Copy logo for web branding if present
        for candidate in ["ALYVON logo.png", "ALYVON logo.jpg", "ALYVON logo.jpeg"]:
            if os.path.exists(candidate):
                try:
                    shutil.copyfile(candidate, os.path.join('web','logo.png'))
                    break
                except Exception as _e:
                    pass
    except Exception as e:
        # Non-blocking: don't crash app if export fails
        print(f"Web feed export error: {e}")
    finally:
        try:
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
