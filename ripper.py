import urllib2
import os
import Tkinter as tk
from BeautifulSoup import *

url = "" #set URL
       
class siteRipper(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Site Ripper")
        self.create_interface()

    def create_interface(self):
        self.geometry("250x260+150+150")
        L1 = tk.Label(text="URL to rip")
        L1.place(x=2, y=4, anchor="nw")
        L2 = tk.Label(text="Output Directory")
        L2.place(x=2, y=26)
        E1 = tk.Entry(self)
        E1.place(x=140, y=30)
        E2 = tk.Entry(self)
        E2.place(x=120, y=8)
        B1 = tk.Button(self, text="Choose", command=self.saveDialog)
        B1.place(x=120, y=26)
        B2 = tk.Button(self, text="Download", command=self.doRip)
        B2.place(x=180, y=230)
        LB1 = tk.Listbox(self)
        LB1.place(x=120, y=60)
        
    def saveDialog(self):
        path = tkFileDialog.asksaveasfilename()
        return path

    def doRip(self):
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html)
        self.getHTML()
        self.getCSS()
        self.getJS()
        self.getIMG()

    def getHTML(self):
        site = urllib2.urlopen(url)
        folder = url.replace(':','').replace('?','')
        data = site.read()
        filename = ('./siteripper/%s/source.txt' %folder, 'w')
        file.writelines(data)
        file.close()
        print data

    def getCSS(self):
        css_files = soup.findAll('link',{'rel':'stylesheet'})
        for css in css_files:
            print url + css['href']

    def getJS(self):
        js_files = soup.findAll('script',{'src':True})
        for js in js_files:
            if js['src'].startswith("//"):
                print js['src']
            else:
                print url + js['src']

    def getIMG(self):
        img_files = soup.findAll('img',{'src':True})
        for img in img_files:
            if img['src'].startswith('http'):
                print img['src']
            else:
                print url + img['src']
        



app = siteRipper()           
app.mainloop()
