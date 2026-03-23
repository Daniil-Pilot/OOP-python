#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk, tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox
import asyncio, aiohttp, json, threading
from datetime import datetime, timezone

class RffGui:
    def __init__(self, root):
        self.root = root
        root.title("Запрос рейса")
        root.geometry("520x600")
        self.build_form(); self.build_tree(); self.build_log()

    def build_form(self):
        frm = ttk.Frame(self.root)
        frm.pack(fill="x", padx=6, pady=6)
        ttk.Label(frm, text="Откуда:").grid(row=0, column=0, sticky="w")
        self.e_orig = ttk.Entry(frm, width=25)
        self.e_orig.grid(row=0, column=1, padx=4)
        self.e_orig.insert(0, "SVO")
        ttk.Label(frm, text="Куда:").grid(row=1, column=0, sticky="w")
        self.e_dest = ttk.Entry(frm, width=25)
        self.e_dest.grid(row=1, column=1, padx=4)
        self.e_dest.insert(0, "LED")
        self.btn = ttk.Button(frm, text="Найти рейсы", command=self.run_search)
        self.btn.grid(row=2, column=0, columnspan=2, pady=8)

    def build_tree(self):
        COLS = ("Цена", "Пересадки", "Длит-ть", "Оценка")
        self.tree = ttk.Treeview(self.root, columns=COLS, show="headings", height=10)
        for c in COLS:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=100)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

    def build_log(self):
        self.log = scrolledtext.ScrolledText(self.root, height=5, state="disabled")
        self.log.pack(fill="x", padx=6, pady=4)

    def log_add(self, txt):
        self.log["state"] = "normal"
        self.log.insert("end", txt + "\n")
        self.log.see("end")
        self.log["state"] = "disabled"

    def run_search(self):
        self.btn["state"] = "disabled"
        self.log_add("Ищу...")
        threading.Thread(target=self._async_wrapper, daemon=True).start()

    def _async_wrapper(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        flights = loop.run_until_complete(self.search_flights())
        self.root.after(0, self.show_results, flights)

    async def search_flights(self):
        origin = self.e_orig.get().strip().upper()
        dest = self.e_dest.get().strip().upper()
        url = f"https://flying-roses-352516.et.r.appspot.com/api/flights?origin={origin}&destination={dest}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("flights", [])
                else:
                    self.root.after(0, messagebox.showerror, "Ошибка", f"HTTP {resp.status}")
                    return []

    def show_results(self, flights):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if not flights:
            self.log_add("Рейсы не найдены")
            self.btn["state"] = "normal"
            return
        for f in flights:
            self.tree.insert("", "end", values=(
                f.get("price", ""),
                f.get("transfers", ""),
                f.get("duration", ""),
                f.get("rating", "")
            ))
        self.log_add(f"Найдено рейсов: {len(flights)}")
        self.btn["state"] = "normal"
        
        # Сохранение JSON
        with open("rff_latest.json", "w", encoding="utf8") as fp:
            json.dump({
                "requested": datetime.now(tz=timezone.utc).isoformat(),
                "origin": self.e_orig.get(),
                "destination": self.e_dest.get(),
                "flights": flights
            }, fp, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    RffGui(root)
    root.mainloop()