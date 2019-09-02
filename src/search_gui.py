import os, re
import tkinter as tk
from bs4 import BeautifulSoup
import index

class gui:
    def __init__(self, master, idx = ""):
        self.master = master
        self.master.title("CS121/INF141 Search Engine")
        self.idx = idx
        self.e1 = tk.Entry(self.master, width=50)
        self.e1.grid(row=1, column=1) 
        self.preview = tk.BooleanVar()
        tk.Label(self.master, text = "Search Engine", font = ('Helvetica',18)).grid(row = 0, column = 1, pady=10)
        tk.Button(self.master, text = "Quit", font = ('Helvetica', 14), command = quit).grid(row = 4, column = 0,sticky = tk.E, padx=5, pady=5)
        tk.Button(self.master, text='Search', font = ('Helvetica', 14), command=self.create_window).grid(row=4, column = 2, sticky = tk.W, padx=5, pady=5) 
        tk.Radiobutton(self.master, text="Previews off", variable=self.preview, value=False).grid(row=2, column=1)
        tk.Radiobutton(self.master, text="Previews on", variable=self.preview, value=True).grid(row=3, column=1)
    
    def create_window(self):
        url_file_dict = self._process_query()
        if url_file_dict != None and url_file_dict != {}:
            self.window = tk.Toplevel(self.master)
            label = tk.Label(self.window, text = "Retrieved Webpages:", font = ('Helvetica', 20))
            label.pack()
            scrollbar = tk.Scrollbar(self.window)
            scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
            my_list = tk.Listbox(self.window, yscrollcommand = scrollbar.set, font = ('Helvetica', 15, 'bold'), width = 200)
            x = 1
            for local, url in url_file_dict.items():
                if x <= 30:
                    my_list.insert(tk.END, str(x) + ': ' + url)
                    ## get brief description for the URL
                    if self.preview.get():
                        brief_descr = self._get_brief_description(local)
                        my_list.insert(tk.END, "    " + "Brief Description: " + brief_descr)
                        my_list.insert(tk.END, "\n")
                x = x+1
            my_list.pack(side = tk.LEFT, fill = tk.BOTH)
            scrollbar.config(command = my_list.yview)

    def _process_query(self):
        if self.e1.get() != '':
            self.idx.query = self.e1.get() if self.e1.get().islower() else self.e1.get().lower()
            self.idx.query = self.idx.query.split(' ')
            return self.idx.rank_results()
    
    def _get_brief_description(self, local_file):
        html_ = open(os.path.join(".", "WEBPAGES_RAW", local_file), encoding = 'utf-8')
        soup = BeautifulSoup(html_, 'html.parser')
        p_tags = soup.findAll(['h1', 'h2', 'h3', 'h4', 'h5', 'h6','p'])
        result = u" · ".join(t.get_text().strip() for t in p_tags if len(t.get_text()) > 2) [:125]
        return result + "..."
 
def main():
    idx = index.Index()
    master = tk.Tk()
    GUI = gui(master, idx)
    master.mainloop()
    
if __name__ == '__main__':
    main()