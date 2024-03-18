from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from PyPDF2 import PdfMerger

root = Tk()

frm = LabelFrame(root, bg='#2f474e')
frm2 = LabelFrame(root, bg="#2f474e")

def load_img():

    global filearr

    fileloc = filedialog.askopenfilenames(parent=frm, title="Select Files", initialdir="C:/", filetypes=(("png files", "*.png"),("jpeg files","*.jpeg"),("jpg files","*.jpg")))
    filearr = list(fileloc)
    
    for i in range(0,len(filearr)):
        Label(frm, text=filearr[i], padx=5, pady=5, font=(20), bg='#2f474e', fg='#91c5d5').grid(row = i+2, column=0)
    
    def show_img(filearr):
        top = Toplevel()
        top.geometry("1000x500")
        image_list = []

        frame = LabelFrame(top)
        frame.pack(fill="both", expand=YES)

        mycanvas = Canvas(frame)
        mycanvas.pack(side="left", fill="both", expand=YES)

        scroll_y = Scrollbar(frame, command=mycanvas.yview)
        scroll_y.pack(side=RIGHT, fill="y")

        mycanvas.configure(yscrollcommand=scroll_y.set)
        

        def configure_scrollregion(event):
            mycanvas.configure(scrollregion=mycanvas.bbox('all'))

        mycanvas.bind("<Configure>", configure_scrollregion)

        canframe = Frame(mycanvas)
        mycanvas.create_window((0,0), window=canframe, anchor='nw')

        for filepath in filearr:
            
            img = Image.open(filepath)

            my_imag = ImageTk.PhotoImage(img)

            image_list.append(my_imag)

            Label(canframe, image = my_imag).pack()
            
        top.mainloop()
    
    show_img(filearr)
    
    
def to_pdf():
    try:    
        global filearr
        des = filearr[0]
        
        des = des.split('.')[0]
        
        des = des.split('/')
        
        finaldes = ""

        for m in range(0,len(des[0:-1])):
            finaldes = finaldes + des[m] + '/' 
        
        merge = PdfMerger()
        dest = []
        for file in filearr:
            image = Image.open(file)
            converted = image.convert('RGB')
            dest.append('{0}.pdf'.format(file.split('.')[-2]))
            converted.save('{0}.pdf'.format(file.split('.')[-2]))
            merge.append('{0}.pdf'.format(file.split('.')[-2]))
       
        merge.write(finaldes+"/final.pdf")
        merge.close()
        Label(frm2, text="Your PDF is created. It is stored in the same diretory of images (with name: final.pdf) \n along with the Individual PDF of each image.", padx=10, pady=10, font=("Arial", 14, "bold"), bg='#2f474e', fg='#1a8cc9').grid(row= 97,column=0)            

    except:
        messagebox.showerror("ERROR","You need to choose some images")
filearr = []

frm.master.minsize(500,200)

Label(root, text="Image to PDF", font=("Arial", 20, "bold"), padx=5, pady=5, fg="#73585b").pack()
Button(frm, text="Load Images", padx=5, pady=5, command=load_img, font=(16)).grid(row=1,column=0)
Button(frm2, text="Convert to PDF", padx=10, pady=10, command=to_pdf,bg='#2f474e', fg='#1a8cc9', font=("Arial", 11, "bold")).grid(row=99, column=0)
Button(frm2, text="EXIT", command=root.destroy,padx=10, pady=10, fg='#f42727',font=(20)).grid(row=100,column=0)

frm.pack()
frm2.pack()
frm.mainloop()
