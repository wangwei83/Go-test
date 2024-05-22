import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MortgageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Mortgage Calculator")

        # Set up the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        # Loan amount
        self.loan_amount_label = tk.Label(self.main_frame, text="贷款金额:")
        self.loan_amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.loan_amount_entry = tk.Entry(self.main_frame)
        self.loan_amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Loan term
        self.loan_term_label = tk.Label(self.main_frame, text="贷款期限:")
        self.loan_term_label.grid(row=1, column=0, padx=5, pady=5)
        self.loan_term_var = tk.StringVar(value="20 年")
        self.loan_term_menu = ttk.Combobox(self.main_frame, textvariable=self.loan_term_var, values=["10 年", "15 年", "20 年", "25 年", "30 年"])
        self.loan_term_menu.grid(row=1, column=1, padx=5, pady=5)

        # Interest rate
        self.interest_rate_label = tk.Label(self.main_frame, text="商贷利率:")
        self.interest_rate_label.grid(row=2, column=0, padx=5, pady=5)
        self.interest_rate_entry = tk.Entry(self.main_frame)
        self.interest_rate_entry.grid(row=2, column=1, padx=5, pady=5)

        # Repayment method
        self.repayment_method_label = tk.Label(self.main_frame, text="还款方式:")
        self.repayment_method_label.grid(row=3, column=0, padx=5, pady=5)
        self.repayment_method_var = tk.StringVar(value="等额本息")
        self.equal_principal_interest = tk.Radiobutton(self.main_frame, text="等额本息", variable=self.repayment_method_var, value="等额本息")
        self.equal_principal_interest.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.equal_principal = tk.Radiobutton(self.main_frame, text="等额本金", variable=self.repayment_method_var, value="等额本金")
        self.equal_principal.grid(row=3, column=1, padx=5, pady=5)

        # Calculate button
        self.calculate_button = tk.Button(self.main_frame, text="计算", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Result display
        self.result_label = tk.Label(self.main_frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=5)

    def calculate(self):
        try:
            loan_amount = float(self.loan_amount_entry.get()) * 10000  # Convert to Yuan
            loan_term = int(self.loan_term_var.get().split()[0])
            interest_rate = float(self.interest_rate_entry.get()) / 100 / 12
            repayment_method = self.repayment_method_var.get()

            if repayment_method == "等额本息":
                total_months = loan_term * 12
                monthly_payment = loan_amount * interest_rate * (1 + interest_rate) ** total_months / ((1 + interest_rate) ** total_months - 1)
                total_payment = monthly_payment * total_months
                self.result_label.config(text=f"每月还款: {monthly_payment:.2f} 元\n总还款金额: {total_payment:.2f} 元")
            else:
                total_months = loan_term * 12
                monthly_principal = loan_amount / total_months
                monthly_payment_first_month = monthly_principal + loan_amount * interest_rate
                monthly_payment_last_month = monthly_principal + (loan_amount - monthly_principal * (total_months - 1)) * interest_rate
                total_payment = (monthly_payment_first_month + monthly_payment_last_month) / 2 * total_months
                self.result_label.config(text=f"首月还款: {monthly_payment_first_month:.2f} 元\n总还款金额: {total_payment:.2f} 元")

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")

if __name__ == "__main__":
    root = tk.Tk()
    app = MortgageCalculator(root)
    root.mainloop()
