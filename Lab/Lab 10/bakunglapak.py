import tkinter as tk
import tkinter.messagebox as tkmsg

# Membuat class product
class Product(object):
    def __init__(self, nama, harga, stok):
        self.__nama = nama
        self.__harga = harga
        self.__stok = stok

    # membuat getter dan setter
    def get_nama(self):
        return self.__nama

    def get_harga(self):
        return self.__harga

    def get_stok(self):
        return self.__stok

    def set_stok(self, jumlah):
        self.__stok -= jumlah

# Mendefinisikan class Buyer
class Buyer(object):
    def __init__(self):
        self.__daftar_beli = {}

    # menambah barang yang dibeli
    def add_daftar_beli(self, produk, jumlah):
        if produk in self.__daftar_beli:
          self.__daftar_beli[produk] += jumlah
        else :
          self.__daftar_beli[produk] = jumlah

    # getter
    def get_daftar_beli(self):
      return self.__daftar_beli



# GUI Starts from here

# Toplevel adalah sebuah class yang mirip dengan Frame namun akan terbuka
# secara terpisah dengan Window utama (jadi membuat top-level window yang
# terpisah)
# Menu LIHAT DAFTAR BARANG
class WindowLihatBarang(tk.Toplevel):
    # Constructor
    def __init__(self, product_dict, master = None):
        super().__init__(master)
        self.product_dict = product_dict
        self.wm_title("Daftar Barang")
        self.create_widgets()

    # Mendefinisikan widget-widget yang ada
    def create_widgets(self):
        self.lbl_judul = tk.Label(self, \
                                  text = 'Daftar Barang Yang Tersedia').grid(row = 0, column = 1)
        self.lbl_nama = tk.Label(self, \
                                 text = 'Nama Produk').grid(row = 1, column = 0)
        self.lbl_harga = tk.Label(self, \
                                  text = 'Harga').grid(row = 1, column = 1)
        self.lbl_stok = tk.Label(self, \
                                 text = 'Stok Produk').grid(row = 1, column = 2)

        # Iterasi untuk menampilkan barang
        i = 2
        for nama, barang in sorted(self.product_dict.items()):
            tk.Label(self, \
                     text = f"{nama}").grid(row = i, column= 0)
            tk.Label(self, \
                     text = f"{barang.get_harga()}").grid(row = i, column= 1)
            tk.Label(self, \
                     text = f"{barang.get_stok()}").grid(row = i, column= 2)
            i += 1

        self.btn_exit = tk.Button(self, text = "EXIT", \
                                  command = self.destroy).grid(row = i, column=1)

# menu BELI
class WindowBeliBarang(tk.Toplevel):
    # Constructor
    def __init__(self, buyer, product_dict, master = None):
        super().__init__(master)
        self.buyer = buyer
        self.product_dict = product_dict
        self.wm_title("Beli Barang")
        self.geometry("280x120")
        self.create_widgets()

    # Mendefinisikan widget-widget yang ada
    def create_widgets(self):
        self.lbl_judul = tk.Label(self, \
                                  text = 'Form Beli Barang').grid(row = 0, column = 1)
        self.lbl_nama = tk.Label(self, \
                                 text = 'Nama Barang').grid(row = 1, column = 0)
        self.nama_barang = tk.StringVar()
        self.ent_nama_barang = tk.Entry(self, textvariable=self.nama_barang, width=20)
        self.ent_nama_barang.grid(row = 1, column = 1)
        self.lbl_jumlah = tk.Label(self, \
                                 text = 'Jumlah').grid(row = 2, column = 0)
        self.jumlah = tk.StringVar()
        self.ent_jumlah = tk.Entry(self, textvariable=self.jumlah, width=20)
        self.ent_jumlah.grid(row = 2, column = 1)
        self.btn_exit = tk.Button(self, text = "BELI", \
                                  command = self.beli_barang).grid(row = 3, column=1)
        self.btn_exit = tk.Button(self, text = "EXIT", \
                                  command = self.destroy).grid(row = 4, column=1)

    # Behavior saat membeli barang
    def beli_barang(self):

        nama_barang = self.nama_barang.get()
        jumlah = int(self.jumlah.get())

        if nama_barang == "":
            res = tkmsg.askretrycancel(title="BarangNotFound", message="Nama barang tidak boleh kosong.")
            if res == True:
                pass
            elif res == False:
                tk.Toplevel.destroy(self)
        
        elif nama_barang not in self.product_dict:
            res = tkmsg.askretrycancel(title="BarangNotFound", message=f"Barang dengan nama {nama_barang} tidak ditemukan dalam BakungLapak.")
            if res == True:
                pass
            elif res == False:
                tk.Toplevel.destroy(self)

        elif self.product_dict[nama_barang].get_stok() - jumlah < 0:
            tkmsg.showwarning(title = "StokEmpty", message="Maaf, stok telah habis.")
        
        else :
            barang = self.product_dict[nama_barang]
            buyer.add_daftar_beli(barang, jumlah)
            barang.set_stok(jumlah)
            self.ent_nama_barang.delete(0, tk.END)
            self.ent_jumlah.delete(0, tk.END)
            tkmsg.showinfo("Berhasil!", f"Berhasil membeli {nama_barang}")

# menu Checkout
class WindowCheckOut(tk.Toplevel):
    # Constructor
    def __init__(self, buyer, master = None):
        super().__init__(master)
        self.wm_title("Daftar Barang")
        self.daftar_dibeli = buyer.get_daftar_beli()
        self.create_widgets()

    # Mendefinisikan widget-widget yang ada
    def create_widgets(self):
        self.lbl_judul = tk.Label(self, \
                                  text = 'Keranjangku').grid(row = 0, column = 1)
        self.lbl_nama = tk.Label(self, \
                                 text = 'Nama Produk').grid(row = 1, column = 0)
        self.lbl_harga = tk.Label(self, \
                                  text = 'Harga Barang').grid(row = 1, column = 1)
        self.lbl_stok = tk.Label(self, \
                                 text = 'Jumlah').grid(row = 1, column = 2)

        # Handling barang belum ada
        if self.daftar_dibeli == {}:
            tk.Label(self, text = "Belum ada barang yang dibeli :(").grid(row = 2, column = 1)
            self.btn_exit = tk.Button(self, text = "EXIT", \
                                    command = self.destroy).grid(row = 3, column=1)
        else:    
            # Iterasi untuk menampilkan barang
            i = 2
            for nama, barang in self.daftar_dibeli.items():
                tk.Label(self, \
                        text = f"{nama.get_nama()}").grid(row = i, column= 0)
                tk.Label(self, \
                        text = f"{nama.get_harga()}").grid(row = i, column= 1)
                tk.Label(self, \
                        text = f"{nama.get_stok()}").grid(row = i, column= 2)
                i += 1

            self.btn_exit = tk.Button(self, text = "EXIT", \
                                    command = self.destroy).grid(row = i, column=1)


# Main Menu
class MainWindow(tk.Frame):
    # Constructor
    def __init__(self, buyer, product_dict, master = None):
        super().__init__(master)
        self.buyer = buyer
        self.product_dict = product_dict
        self.pack()
        self.create_widgets()

    # Mendefinisikan widget-widget yang ada
    def create_widgets(self):
        self.label = tk.Label(self, \
                              text = 'Selamat datang di BakungLapak. Silahkan pilih Menu yang tersedia')

        self.btn_lihat_daftar_barang = tk.Button(self, \
                                                 text = "LIHAT DAFTAR BARANG", \
                                                 command = self.popup_lihat_barang)
        self.btn_beli_barang = tk.Button(self, \
                                         text = "BELI BARANG", \
                                         command = self.popup_beli_barang)
        self.btn_check_out = tk.Button(self, \
                                       text = "CHECK OUT", \
                                       command = self.popup_check_out)
        self.btn_exit = tk.Button(self, \
                                  text = "EXIT", \
                                  command = self.master.destroy)

        self.label.pack()
        self.btn_lihat_daftar_barang.pack()
        self.btn_beli_barang.pack()
        self.btn_check_out.pack()
        self.btn_exit.pack()

    # semua barang yand dijual
    def popup_lihat_barang(self):
        WindowLihatBarang(self.product_dict)

    # menu beli barang
    def popup_beli_barang(self):
        WindowBeliBarang(self.buyer, self.product_dict)

    # menu riwayat barang yang dibeli
    def popup_check_out(self):
        WindowCheckOut(self.buyer)

if __name__ == "__main__":

    buyer = Buyer()

    product_dict = {"Kebahagiaan" : Product("Kebahagiaan", 999999, 1),
                    "Kunci TP3 SDA" : Product("Kunci TP3 SDA", 1000000, 660)}

    m = MainWindow(buyer, product_dict)
    m.master.title("BakungLapak")
    m.master.mainloop()
