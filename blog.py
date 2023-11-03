import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

blogs = []

update_index = -1  # Initialize the update_index variable

def add_blog():
    date = date_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    content = content_text.get("1.0", tk.END)

    if not date or not title or not author or not content:
        return

    # Check if the content already exists in blogs
    content_exists = any(blog["Content"] == content for blog in blogs)

    if not content_exists:
        # Validate the date format using a function
        if not validate_date_format(date):
            messagebox.showerror("Invalid Date", "Please enter a valid date in DD/MM/YYYY format")
            return

        blog = {
            "Date": date,
            "Title": title,
            "Author": author,
            "Content": content
        }

        # Add the new blog at the beginning to display the latest at the top
        blogs.insert(0, blog)

        clear_fields()
        update_second_page_content()

def validate_date_format(date):
    try:
        day, month, year = map(int, date.split('/'))
        if (2020 <= year <= 2099) and (1 <= month <= 12) and (1 <= day <= 31):
            return True
        else:
            return False
    except ValueError:
        return False

def clear_fields():
    date_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

def update_second_page_content():
    for widget in second_frame.winfo_children():
        widget.destroy()

    for index, blog in enumerate(blogs):
        blog_frame = tk.Frame(second_frame, bg="light pink", padx=10, pady=10, relief=tk.SOLID, borderwidth=2)
        blog_frame.pack(fill="x", padx=10, pady=10)

        date_label = tk.Label(blog_frame, text=f"Date: {blog['Date']}", font=("Arial", 14, "bold"), bg="light pink")
        date_label.pack(anchor="w")
        title_label = tk.Label(blog_frame, text=f"Title: {blog['Title']}", font=("Arial", 14, "bold"), bg="light pink")
        title_label.pack(anchor="w")
        author_label = tk.Label(blog_frame, text=f"Author: {blog['Author']}", font=("Arial", 14, "bold"), bg="light pink")
        author_label.pack(anchor="w")

        content_label = tk.Label(blog_frame, text="Content:", font=("Arial", 14, "bold"), bg="light pink")
        content_label.pack(anchor="w")

        content_text = scrolledtext.ScrolledText(blog_frame, wrap=tk.WORD, width=100, height=10, font=("Arial", 12))
        content_text.insert(tk.INSERT, blog['Content'])
        content_text.pack(padx=5, pady=5)

        delete_button = tk.Button(blog_frame, text="Delete", command=lambda index=index: delete_blog(index), font=("Arial", 12))
        delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        update_button = tk.Button(blog_frame, text="Update", command=lambda index=index: update_blog(index), font=("Arial", 12))
        update_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Update the canvas to accommodate the new content
    second_canvas.update_idletasks()
    second_canvas.config(scrollregion=second_canvas.bbox("all"))

def delete_blog(index):
    # Display a confirmation message
    confirm = messagebox.askyesno("Delete Blog", "Are you sure you want to delete this blog?")
    
    if confirm:
        del blogs[index]
        update_second_page_content()

def update_blog(index):
    global update_index
    update_index = index

    update_date_entry.delete(0, tk.END)
    update_date_entry.insert(0, blogs[index]["Date"])
    update_title_entry.delete(0, tk.END)
    update_title_entry.insert(0, blogs[index]["Title"])
    update_author_entry.delete(0, tk.END)
    update_author_entry.insert(0, blogs[index]["Author"])
    update_content_text.delete("1.0", tk.END)
    update_content_text.insert(tk.INSERT, blogs[index]["Content"])

    notebook.select(third_page)

def clear_update_fields():
    update_date_entry.delete(0, tk.END)
    update_title_entry.delete(0, tk.END)
    update_author_entry.delete(0, tk.END)
    update_content_text.delete("1.0", tk.END)

def save_updated_blog():
    updated_date = update_date_entry.get()
    updated_title = update_title_entry.get()
    updated_author = update_author_entry.get()
    updated_content = update_content_text.get("1.0", tk.END)

    if not updated_date or not updated_title or not updated_author or not updated_content:
        return

    blogs[update_index] = {
        "Date": updated_date,
        "Title": updated_title,
        "Author": updated_author,
        "Content": updated_content
    }

    update_second_page_content()
    clear_update_fields()  # Clear the fields on the third page
    notebook.select(second_page)

root = tk.Tk()
root.title("Blog Application")
root.geometry("4000x4000")
root.configure(bg="light pink")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

input_frame = tk.Frame(notebook, bg="light pink")
notebook.add(input_frame, text="Add Blog")

font_style = ("Arial", 20)
label_font = ("Arial", 20)
entry_font = ("Arial", 16)
#lb_bg = '#E6E6FA'
#lb_bg = '#AEEEEE'
lb_bg = '#40E0D0'
date_label = tk.Label(input_frame, text="Date", font=label_font, bg = lb_bg)
date_label.pack()
date_entry = tk.Entry(input_frame, font=entry_font)
date_entry.pack(padx=5, pady=10)
date_entry.config(fg="black")

title_label = tk.Label(input_frame, text="Title", font=label_font, bg = lb_bg)
title_label.pack()
title_entry = tk.Entry(input_frame, font=entry_font)
title_entry.pack(padx=5, pady=10)
title_entry.config(fg="black")

author_label = tk.Label(input_frame, text="Author", font=label_font, bg = lb_bg)
author_label.pack()
author_entry = tk.Entry(input_frame, font=entry_font)
author_entry.pack(padx=5, pady=10)
author_entry.config(fg="black")

content_label = tk.Label(input_frame, text="Content", font=label_font, bg = lb_bg)
content_label.pack()
content_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=100, height=17, font=entry_font)
content_text.pack(padx=5, pady=10)
content_text.config(fg="black")

add_blog_button = tk.Button(input_frame, text="Add Blog", command=add_blog, font=("Arial", 18), bg='#40E0D0')
add_blog_button.pack()

second_page = ttk.Frame(notebook)
notebook.add(second_page, text="Second Page")

# Create a Canvas for the Second Page
second_canvas = tk.Canvas(second_page)
second_canvas.pack(side=tk.LEFT, fill="both", expand=True)

# Create a Vertical Scrollbar for the Second Canvas
second_scrollbar = ttk.Scrollbar(second_page, orient="vertical", command=second_canvas.yview)
second_scrollbar.pack(side=tk.RIGHT, fill="y")
second_canvas.configure(yscrollcommand=second_scrollbar.set)

# Create a Frame inside the Second Canvas
second_frame = tk.Frame(second_canvas, bg="light pink")
second_canvas.create_window((0, 0), window=second_frame, anchor="nw")

second_frame.bind("<Configure>", lambda e: second_canvas.configure(scrollregion=second_canvas.bbox("all")))

second_canvas.bind("<Configure>", lambda e: second_canvas.itemconfig(second_frame_id, width=e.width))
second_frame_id = second_canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Initialize the second page content
update_second_page_content()

style = ttk.Style()
style.configure("TFrame", background="light pink")

third_page = ttk.Frame(notebook, style="TFrame")
notebook.add(third_page, text="Third Page")

update_date_label = tk.Label(third_page, text="Date", font=label_font)
update_date_label.pack()
update_date_entry = tk.Entry(third_page, font=entry_font)
update_date_entry.pack(padx=5, pady=5)

update_title_label = tk.Label(third_page, text="Title", font=label_font)
update_title_label.pack()
update_title_entry = tk.Entry(third_page, font=entry_font)
update_title_entry.pack(padx=5, pady=5)

update_author_label = tk.Label(third_page, text="Author", font=label_font)
update_author_label.pack()
update_author_entry = tk.Entry(third_page, font=entry_font)
update_author_entry.pack(padx=5, pady=5)

update_content_label = tk.Label(third_page, text="Content", font=label_font)
update_content_label.pack()
update_content_text = scrolledtext.ScrolledText(third_page, wrap=tk.WORD, width=134, height=18, font=("Arial", 12))
update_content_text.pack(padx=5, pady=5)

update_save_button = tk.Button(third_page, text="Save Update", command=save_updated_blog, font=("Arial", 17))
update_save_button.pack()

root.mainloop()