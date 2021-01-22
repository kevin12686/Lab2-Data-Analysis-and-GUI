import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from population import Population


class MainPlotWindows(tk.Frame):
    def __init__(self, master=None):
        try:
            super().__init__(master)
            self.master = master
            for i in range(2):
                tk.Grid.rowconfigure(master, i, weight=1)
            for i in range(4):
                tk.Grid.columnconfigure(master, i, weight=1)
            self.init_window()
            self.population = Population('references//years.csv', 'references//countries.csv', 'references//population.csv')
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.master.destroy()

    def init_window(self):
        self.master.title('Population')
        title_lab = tk.Label(self.master, text='Population of Countries', font=('Calibri', 20))
        title_lab.grid(row=0, column=0, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        region_btn = tk.Button(self.master, text='By Region', font=('Calibri', 14))
        region_btn.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        region_btn.bind('<Button-1>', lambda e: self.fn_region())
        t10_btn = tk.Button(self.master, text='Top 10', font=('Calibri', 14))
        t10_btn.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        t10_btn.bind('<Button-1>', lambda e: self.fn_top10())
        countries_btn = tk.Button(self.master, text='By Countries', font=('Calibri', 14))
        countries_btn.grid(row=1, column=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        countries_btn.bind('<Button-1>', lambda e: self.fn_countries())
        gwt2_btn = tk.Button(self.master, text='Growth Top 2', font=('Calibri', 14))
        gwt2_btn.grid(row=1, column=3, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        gwt2_btn.bind('<Button-1>', lambda e: self.fn_gwtop2())

    def fn_region(self):
        try:
            fig, _ = self.population.figure_regions_trends()
            PlotWindows(fig, self.master)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def fn_top10(self):
        try:
            fig, _ = self.population.figure_top10_trends()
            PlotWindows(fig, master=self.master)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def fn_countries(self):
        try:
            DialogPlotWindows(self.population.get_countries(), self.population.figure_select_trends, self.master)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def fn_gwtop2(self):
        try:
            fig, _ = self.population.figure_gtop2_trends()
            PlotWindows(fig, self.master)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))


class DialogPlotWindows(tk.Toplevel):
    def __init__(self, countries_list, figure_fn, master=None):
        try:
            super().__init__(master)
            self.title('Dialog')
            self.grab_set()
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            lb = tk.Listbox(self, font=('Calibri', 14), selectmode=tk.MULTIPLE)
            for i in range(countries_list.size):
                lb.insert(i, countries_list[i])
            lb.grid(row=0, column=0, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc = tk.Scrollbar(self, orient='vertical')
            sc.grid(row=0, column=1, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            sc.config(command=lb.yview)
            lb.config(yscrollcommand=sc.set)
            cf_btn = tk.Button(self, text='Confirm', font=('Calibri', 14))
            cf_btn.grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
            cf_btn.bind('<Button-1>', lambda event: self.fn_countries(list(lb.curselection()), figure_fn))
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.destroy()

    def fn_countries(self, idx, fn):
        try:
            fig = fn(list(idx))
            PlotWindows(fig, self.master)
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))


class PlotWindows(tk.Toplevel):
    def __init__(self, figure, master=None):
        try:
            super().__init__(master)
            self.title('Plot')
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            canvas = FigureCanvasTkAgg(figure, master=self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, columnspan=5, padx=(5, 5), pady=(5, 5), sticky=tk.NSEW)
        except Exception as e:
            tk.messagebox.showerror('Error', str(e))
            self.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = MainPlotWindows(master=root)
    app.mainloop()
