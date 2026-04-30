
import tkinter as tk
from tkinter import ttk, messagebox
from knapsack import knapsack
from items_data import SAMPLE_ITEMS
import copy

BG_DARK     = "#0f1117"
BG_CARD     = "#1a1d27"
BG_INPUT    = "#22263a"
ACCENT      = "#4f8ef7"
ACCENT2     = "#34d399"
DANGER      = "#f87171"
TEXT_WHITE  = "#f1f5f9"
TEXT_MUTED  = "#94a3b8"
BORDER      = "#2e3347"

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEAD   = ("Courier New", 12, "bold")
FONT_BODY   = ("Courier New", 10)
FONT_SMALL  = ("Courier New", 9)


class SmartBudgetPlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💰 Smart Budget Planner — Dynamic Programming")
        self.geometry("1100x750")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # App state
        self.custom_items = copy.deepcopy(SAMPLE_ITEMS)
        self.result_items = []

        self._build_ui()

    # ──────────────────────────────────────────
    #  UI BUILD
    # ──────────────────────────────────────────
    def _build_ui(self):
        # ── Title Bar ──
        title_frame = tk.Frame(self, bg=BG_DARK, pady=16)
        title_frame.pack(fill="x")

        tk.Label(title_frame, text="💰 Smart Budget Planner",
                 font=FONT_TITLE, fg=ACCENT, bg=BG_DARK).pack()
        tk.Label(title_frame, text="Powered by 0/1 Knapsack Dynamic Programming",
                 font=FONT_SMALL, fg=TEXT_MUTED, bg=BG_DARK).pack()

        # ── Main 3-column layout ──
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=1)
        main.columnconfigure(2, weight=2)
        main.rowconfigure(0, weight=1)

        self._build_items_panel(main)
        self._build_control_panel(main)
        self._build_result_panel(main)

    def _card(self, parent, title, col, row=0, colspan=1):
        """Helper: creates a styled card frame."""
        outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        outer.grid(row=row, column=col, columnspan=colspan,
                   sticky="nsew", padx=6, pady=6)
        inner = tk.Frame(outer, bg=BG_CARD)
        inner.pack(fill="both", expand=True)
        tk.Label(inner, text=title, font=FONT_HEAD,
                 fg=ACCENT, bg=BG_CARD, pady=8).pack(fill="x", padx=12)
        sep = tk.Frame(inner, bg=BORDER, height=1)
        sep.pack(fill="x")
        return inner

    # ── LEFT: Items List ──────────────────────
    def _build_items_panel(self, parent):
        card = self._card(parent, "🛒  Available Items", col=0)

        # Treeview
        cols = ("Item", "Price (₹)", "Value Score")
        tree_frame = tk.Frame(card, bg=BG_CARD)
        tree_frame.pack(fill="both", expand=True, padx=12, pady=8)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                         background=BG_INPUT, foreground=TEXT_WHITE,
                         fieldbackground=BG_INPUT, rowheight=26,
                         font=FONT_BODY, borderwidth=0)
        style.configure("Treeview.Heading",
                         background=BG_DARK, foreground=ACCENT,
                         font=FONT_HEAD, relief="flat")
        style.map("Treeview", background=[("selected", ACCENT)])

        self.tree = ttk.Treeview(tree_frame, columns=cols,
                                  show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=120)
        self.tree.column("Item", anchor="w", width=160)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                   command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self._refresh_tree()

        # Add-item controls
        add_frame = tk.Frame(card, bg=BG_CARD, pady=8)
        add_frame.pack(fill="x", padx=12)

        tk.Label(add_frame, text="Add Custom Item",
                 font=FONT_HEAD, fg=ACCENT2, bg=BG_CARD).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 4))

        labels = ["Name", "Price (₹)", "Value (1-100)"]
        self.add_entries = []
        for j, lbl in enumerate(labels):
            tk.Label(add_frame, text=lbl, font=FONT_SMALL,
                     fg=TEXT_MUTED, bg=BG_CARD).grid(row=1, column=j, padx=4)
            e = tk.Entry(add_frame, bg=BG_INPUT, fg=TEXT_WHITE,
                         insertbackground=TEXT_WHITE, font=FONT_BODY,
                         relief="flat", width=12)
            e.grid(row=2, column=j, padx=4, pady=2)
            self.add_entries.append(e)

        tk.Button(add_frame, text="➕ Add", font=FONT_BODY,
                  bg=ACCENT2, fg=BG_DARK, relief="flat",
                  padx=8, command=self._add_item).grid(
            row=2, column=3, padx=4)

    # ── MIDDLE: Controls ──────────────────────
    def _build_control_panel(self, parent):
        card = self._card(parent, "⚙️  Settings", col=1)

        pad = dict(padx=12, pady=6, fill="x")

        tk.Label(card, text="Your Budget (₹)", font=FONT_BODY,
                 fg=TEXT_MUTED, bg=BG_CARD).pack(**pad)

        self.budget_var = tk.StringVar(value="10000")
        budget_entry = tk.Entry(card, textvariable=self.budget_var,
                                 font=("Courier New", 14, "bold"),
                                 bg=BG_INPUT, fg=ACCENT2,
                                 insertbackground=ACCENT2,
                                 relief="flat", justify="center")
        budget_entry.pack(padx=12, pady=2, fill="x")

        # Quick budget buttons
        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(padx=12, pady=4, fill="x")
        for amt in [5000, 10000, 25000, 50000]:
            tk.Button(btn_row, text=f"₹{amt//1000}k",
                      font=FONT_SMALL, bg=BG_INPUT, fg=TEXT_WHITE,
                      relief="flat", padx=4,
                      command=lambda a=amt: self.budget_var.set(str(a))
                      ).pack(side="left", expand=True, fill="x", padx=2)

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)

        # Run button
        tk.Button(card, text="🚀 Find Best\n   Items",
                  font=FONT_HEAD, bg=ACCENT, fg="white",
                  relief="flat", pady=12, cursor="hand2",
                  command=self._run_knapsack
                  ).pack(padx=12, pady=4, fill="x")

        # Reset button
        tk.Button(card, text="🔄 Reset Items",
                  font=FONT_BODY, bg=BG_INPUT, fg=TEXT_MUTED,
                  relief="flat", pady=6,
                  command=self._reset_items
                  ).pack(padx=12, pady=4, fill="x")

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)

        # Stats labels
        tk.Label(card, text="Last Result", font=FONT_HEAD,
                 fg=TEXT_MUTED, bg=BG_CARD).pack(padx=12, anchor="w")

        self.stat_items = tk.StringVar(value="Items selected: —")
        self.stat_spent = tk.StringVar(value="Total spent: —")
        self.stat_value = tk.StringVar(value="Total value: —")
        self.stat_saved = tk.StringVar(value="Savings: —")

        for var in [self.stat_items, self.stat_spent,
                    self.stat_value, self.stat_saved]:
            tk.Label(card, textvariable=var, font=FONT_SMALL,
                     fg=ACCENT2, bg=BG_CARD, anchor="w").pack(
                padx=14, pady=1, fill="x")

        # DP explanation
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=12, pady=10)
        tk.Label(card, text="How DP Works",
                 font=FONT_HEAD, fg=TEXT_MUTED, bg=BG_CARD).pack(
            padx=12, anchor="w")
        explain = (
            "1. Build a table of\n"
            "   size items × budget\n\n"
            "2. For each item decide:\n"
            "   Take it or skip it?\n\n"
            "3. Choose the option\n"
            "   with higher value\n\n"
            "4. Trace back the table\n"
            "   to find chosen items"
        )
        tk.Label(card, text=explain, font=FONT_SMALL,
                 fg=TEXT_MUTED, bg=BG_CARD, justify="left").pack(
            padx=14, anchor="w")

    # ── RIGHT: Results ────────────────────────
    def _build_result_panel(self, parent):
        card = self._card(parent, "✅  Best Items to Buy", col=2)

        self.result_frame = tk.Frame(card, bg=BG_CARD)
        self.result_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self._show_placeholder()

    def _show_placeholder(self):
        for w in self.result_frame.winfo_children():
            w.destroy()
        tk.Label(self.result_frame,
                 text="\n\n\n🎯\n\nSet your budget\nand click\n🚀 Find Best Items\nto see results!",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_CARD,
                 justify="center").pack(expand=True)

    # ──────────────────────────────────────────
    #  LOGIC
    # ──────────────────────────────────────────
    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.custom_items:
            self.tree.insert("", "end", values=(
                item['name'],
                f"₹{item['price']:,}",
                item['value']
            ))

    def _add_item(self):
        name_e, price_e, val_e = self.add_entries
        name = name_e.get().strip()
        try:
            price = int(price_e.get().strip())
            value = int(val_e.get().strip())
            assert 1 <= value <= 100
            assert price > 0
            assert name
        except Exception:
            messagebox.showerror("Invalid Input",
                "Please enter:\n• A non-empty name\n"
                "• Price as a positive number\n"
                "• Value between 1 and 100")
            return

        self.custom_items.append({"name": name, "price": price, "value": value})
        self._refresh_tree()
        for e in self.add_entries:
            e.delete(0, tk.END)

    def _reset_items(self):
        self.custom_items = copy.deepcopy(SAMPLE_ITEMS)
        self._refresh_tree()
        self._show_placeholder()
        for var in [self.stat_items, self.stat_spent,
                    self.stat_value, self.stat_saved]:
            var.set(var.get().split(":")[0] + ": —")

    def _run_knapsack(self):
        try:
            budget = int(self.budget_var.get().strip())
            assert budget > 0
        except Exception:
            messagebox.showerror("Invalid Budget",
                                 "Please enter a positive integer budget.")
            return

        if not self.custom_items:
            messagebox.showinfo("No Items", "Please add some items first.")
            return

        max_val, selected, dp_table = knapsack(budget, self.custom_items)

        total_spent = sum(i['price'] for i in selected)
        savings = budget - total_spent
        self.stat_items.set(f"Items selected: {len(selected)}")
        self.stat_spent.set(f"Total spent: ₹{total_spent:,}")
        self.stat_value.set(f"Total value: {max_val} pts")
        self.stat_saved.set(f"Savings: ₹{savings:,}")

        self._show_results(selected, total_spent, max_val, budget, savings)

    def _show_results(self, items, spent, value, budget, savings):
        for w in self.result_frame.winfo_children():
            w.destroy()

        if not items:
            tk.Label(self.result_frame,
                     text="😕 No items fit within this budget.\nTry a higher budget!",
                     font=FONT_BODY, fg=DANGER, bg=BG_CARD).pack(expand=True)
            return
        summary = tk.Frame(self.result_frame, bg=BG_INPUT, pady=8)
        summary.pack(fill="x", pady=(0, 8))

        info = [
            ("Budget", f"₹{budget:,}", TEXT_MUTED),
            ("Spent",  f"₹{spent:,}", DANGER),
            ("Saved",  f"₹{savings:,}", ACCENT2),
            ("Value",  f"{value} pts", ACCENT),
        ]
        for label, val, color in info:
            col = tk.Frame(summary, bg=BG_INPUT)
            col.pack(side="left", expand=True)
            tk.Label(col, text=val, font=("Courier New", 11, "bold"),
                     fg=color, bg=BG_INPUT).pack()
            tk.Label(col, text=label, font=FONT_SMALL,
                     fg=TEXT_MUTED, bg=BG_INPUT).pack()
        canvas = tk.Canvas(self.result_frame, bg=BG_CARD,
                            highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical",
                                   command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=BG_CARD)

        scroll_frame.bind("<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, item in enumerate(items, 1):
            row = tk.Frame(scroll_frame, bg=BG_INPUT, pady=6, padx=10)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=f"{i}. {item['name']}",
                     font=FONT_HEAD, fg=TEXT_WHITE, bg=BG_INPUT,
                     anchor="w").grid(row=0, column=0, sticky="w")

            tk.Label(row, text=f"₹{item['price']:,}",
                     font=FONT_BODY, fg=DANGER, bg=BG_INPUT).grid(
                row=0, column=1, padx=20)

            tk.Label(row, text=f"⭐ {item['value']} pts",
                     font=FONT_BODY, fg=ACCENT, bg=BG_INPUT).grid(
                row=0, column=2)

            bar_bg = tk.Frame(row, bg=BORDER, height=4, width=160)
            bar_bg.grid(row=1, column=0, columnspan=3, sticky="w", pady=(3, 0))
            bar_fill = tk.Frame(row, bg=ACCENT2, height=4,
                                width=int(item['value'] * 1.6))
            bar_fill.grid(row=1, column=0, columnspan=3, sticky="w", pady=(3, 0))


if __name__ == "__main__":
    app = SmartBudgetPlanner()
    app.mainloop()