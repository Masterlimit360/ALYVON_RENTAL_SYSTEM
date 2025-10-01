"""
Improved rental management system with Ghana Cedis currency and multiple item support.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date, timedelta
from database import SessionLocal, Item, Customer, Rental, init_database
from sqlalchemy.orm import Session
from PIL import Image, ImageTk
import os

class RentalManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALYVON Rental Management System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Set window icon
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
        # Header with logo
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Try to load and display logo
        try:
            logo_image = Image.open("ALYVON logo.png")
            logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = tk.Label(header_frame, image=self.logo_photo, bg='#2c3e50')
            logo_label.pack(side='left', padx=10, pady=10)
        except:
            # If logo fails to load, just show text
            logo_label = tk.Label(header_frame, text="ALYVON", font=("Arial", 16, "bold"), 
                                fg='white', bg='#2c3e50')
            logo_label.pack(side='left', padx=10, pady=10)
        
        # Title
        title_label = tk.Label(header_frame, text="Rental Management System", 
                              font=("Arial", 16, "bold"), fg='white', bg='#2c3e50')
        title_label.pack(side='left', padx=20, pady=10)
        
        # Currency label
        currency_label = tk.Label(header_frame, text="Currency: Ghana Cedis (GHS)", 
                                font=("Arial", 10), fg='#ecf0f1', bg='#2c3e50')
        currency_label.pack(side='right', padx=20, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_rental_tab()
        self.create_inventory_tab()
        self.create_customers_tab()
        self.create_reports_tab()
        self.create_history_tab()
        
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Dashboard content
        tk.Label(dashboard_frame, text="Rental System Overview", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Summary frame
        summary_frame = tk.Frame(dashboard_frame, bg='white', relief='raised', bd=2)
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        # Get summary data
        db = SessionLocal()
        try:
            total_items = db.query(Item).count()
            total_customers = db.query(Customer).count()
            active_rentals = db.query(Rental).filter(Rental.is_returned == False).count()
            total_rentals = db.query(Rental).count()
            
            tk.Label(summary_frame, text=f"Total Items: {total_items}", 
                    font=("Arial", 12), bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(summary_frame, text=f"Total Customers: {total_customers}", 
                    font=("Arial", 12), bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(summary_frame, text=f"Active Rentals: {active_rentals}", 
                    font=("Arial", 12), bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(summary_frame, text=f"Total Rentals: {total_rentals}", 
                    font=("Arial", 12), bg='white').pack(anchor='w', padx=10, pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dashboard data: {e}")
        finally:
            db.close()
            
        # Refresh button
        tk.Button(dashboard_frame, text="Refresh Dashboard", 
                 command=self.refresh_dashboard).pack(pady=10)
    
    def create_rental_tab(self):
        """Create rental management tab with multiple item support"""
        rental_frame = ttk.Frame(self.notebook)
        self.notebook.add(rental_frame, text="New Rental")
        
        # Customer selection
        customer_frame = tk.LabelFrame(rental_frame, text="Customer Information", 
                                     font=("Arial", 12, "bold"))
        customer_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(customer_frame, text="Customer Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.customer_name_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(customer_frame, text="Phone:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.customer_phone_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_phone_var, width=20).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(customer_frame, text="Address:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.customer_address_var = tk.StringVar()
        tk.Entry(customer_frame, textvariable=self.customer_address_var, width=50).grid(row=1, column=1, columnspan=3, sticky='ew', padx=5, pady=5)
        
        # Item selection for multiple items
        item_frame = tk.LabelFrame(rental_frame, text="Add Items to Rental", 
                                 font=("Arial", 12, "bold"))
        item_frame.pack(fill='x', padx=10, pady=5)
        
        # Item selection controls
        controls_frame = tk.Frame(item_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
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
        period_frame = tk.LabelFrame(rental_frame, text="Rental Period", 
                                   font=("Arial", 12, "bold"))
        period_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(period_frame, text="Start Date:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.start_date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
        tk.Entry(period_frame, textvariable=self.start_date_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(period_frame, text="Number of Days:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.days_var = tk.StringVar(value="1")
        tk.Spinbox(period_frame, from_=1, to=365, textvariable=self.days_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        self.days_var.trace('w', self.calculate_total)
        
        # Pricing
        pricing_frame = tk.LabelFrame(rental_frame, text="Pricing (Ghana Cedis)", 
                                    font=("Arial", 12, "bold"))
        pricing_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(pricing_frame, text="Total Amount:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.total_amount_var = tk.StringVar()
        tk.Label(pricing_frame, textvariable=self.total_amount_var, font=("Arial", 14, "bold"), 
                fg='green').grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(rental_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(button_frame, text="Create Rental", command=self.create_rental, 
                 bg='#27ae60', fg='white', font=("Arial", 12, "bold")).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Form", command=self.clear_rental_form, 
                 bg='#e74c3c', fg='white', font=("Arial", 12, "bold")).pack(side='left', padx=5)
        
        # Load items
        self.load_items()
    
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
        
        # Buttons
        button_frame = tk.Frame(inventory_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(button_frame, text="Refresh Inventory", command=self.refresh_inventory).pack(side='left', padx=5)
        tk.Button(button_frame, text="Add New Item", command=self.add_new_item).pack(side='left', padx=5)
        
        # Load inventory
        self.refresh_inventory()
    
    def create_customers_tab(self):
        """Create customers management tab"""
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="Customers")
        
        # Customers tree
        columns = ('ID', 'Name', 'Phone', 'Email', 'Address', 'Created')
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
        
        # Load customers
        self.refresh_customers()
    
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
        """Calculate total rental amount"""
        try:
            days = int(self.days_var.get()) if self.days_var.get() else 0
            total = 0
            
            for rental_item in self.rental_items:
                item = rental_item['item']
                quantity = rental_item['quantity']
                total += item.daily_rate * quantity * days
            
            self.total_amount_var.set(f"GHS {total:.2f}")
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
                        address=self.customer_address_var.get()
                    )
                    db.add(customer)
                    db.flush()
                
                # Create rental for each item
                total_amount = 0
                start_date = datetime.strptime(self.start_date_var.get(), '%Y-%m-%d').date()
                return_date = start_date + timedelta(days=days)
                
                for rental_item in self.rental_items:
                    item = rental_item['item']
                    quantity = rental_item['quantity']
                    
                    # Check availability again
                    if item.available_quantity < quantity:
                        messagebox.showerror("Error", f"Not enough {item.name} available. Only {item.available_quantity} available")
                        return
                    
                    # Create rental record
                    rental = Rental(
                        customer_id=customer.id,
                        item_id=item.id,
                        quantity=quantity,
                        rental_date=start_date,
                        return_date=return_date,
                        daily_rate=item.daily_rate,
                        total_amount=item.daily_rate * quantity * days
                    )
                    
                    db.add(rental)
                    
                    # Update available quantity
                    item.available_quantity -= quantity
                    total_amount += rental.total_amount
                
                db.commit()
                
                messagebox.showinfo("Success", f"Rental created successfully!\nTotal Amount: GHS {total_amount:.2f}")
                self.clear_rental_form()
                self.refresh_inventory()
                self.refresh_rentals()
                
            except Exception as e:
                db.rollback()
                messagebox.showerror("Error", f"Failed to create rental: {e}")
            finally:
                db.close()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for days")
    
    def clear_rental_form(self):
        """Clear the rental form"""
        self.customer_name_var.set("")
        self.customer_phone_var.set("")
        self.customer_address_var.set("")
        self.item_var.set("")
        self.quantity_var.set("1")
        self.start_date_var.set(date.today().strftime('%Y-%m-%d'))
        self.days_var.set("1")
        self.total_amount_var.set("GHS 0.00")
        self.rental_items = []
        self.update_rental_items_display()
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        # This would refresh the dashboard tab
        pass
    
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
            messagebox.showerror("Error", f"Failed to load inventory: {e}")
        finally:
            db.close()
    
    def refresh_customers(self):
        """Refresh customers display"""
        # Clear existing customers
        for customer in self.customers_tree.get_children():
            self.customers_tree.delete(customer)
        
        db = SessionLocal()
        try:
            customers = db.query(Customer).all()
            for customer in customers:
                self.customers_tree.insert('', 'end', values=(
                    customer.id,
                    customer.name,
                    customer.phone or "",
                    customer.email or "",
                    customer.address or "",
                    customer.created_at.strftime('%Y-%m-%d')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers: {e}")
        finally:
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
            messagebox.showerror("Error", f"Failed to load rentals: {e}")
        finally:
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
            messagebox.showerror("Error", f"Failed to load rental history: {e}")
        finally:
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

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = RentalManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
