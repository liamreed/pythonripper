import urllib2 #urllib2 required for fetching information from ripURL
import Tkinter as tk #import Tkinter for GUI components
import tkFileDialog #import tkFileDialog for Open Directory window
from BeautifulSoup import * #import BeautifulSoup library for HTML scraping
       
class siteRipper(tk.Tk): #init window
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Site Ripper")
        self.create_interface() #init GUI widgets

    def create_interface(self):
        self.geometry("250x250+150+150") #set size of window
        L1 = tk.Label(text="URL to rip")
        L1.place(x=2, y=4, anchor="nw")
        L2 = tk.Label(text="Output Directory")
        L2.place(x=2, y=26)
        L3 = tk.Label()
        L3.place(x=140, y=210)
        E1 = tk.Entry(self, text=self.saveDialog)
        E1.place(x=120, y=6)
        E2 = tk.Entry(self, width=15)
        E2.place(x=150, y=30)
        LB1 = tk.Listbox(self)
        LB1.place(x=120, y=52)
        B1 = tk.Button(self, text="Dir", command=self.saveDialog) #Dir button fires saveDialog method
        B1.place(x=120, y=26)
        B2 = tk.Button(self, text="Download", command=self.doRip) #Download button fires doRip method
        B2.place(x=180, y=220)
        
    def saveDialog(self):
        path = tkFileDialog.askdirectory()
        return path

    def doRip(self):
        ripURL = create_interface.E1.get() #get text from Entry 1
        if ripURL != None: #check if ripURL is empty
            html = urllib2.urlopen(ripURL).read()
            soup = BeautifulSoup(html)
            self.getHTML() #get HTML source of page
            self.getCSS() #get full CSS links from page
            self.getJS() #get full JS links from page
            self.getIMG() #get full IMG links from page
        else:
            create_interface.L3.text = "URL field was empty" #report error to user via L3 label

    def getHTML(self):
        site = urllib2.urlopen(ripURL) #open URL inputted in E1 Entry
        data = site.read()
        filename = ('./siteripper/%s/source.txt', 'w')
        file.writelines(data) #save HTML source to disk
        file.close()
        print data #print HTML to console (debug)

    def getCSS(self):
        css_files = soup.findAll('link',{'rel':'stylesheet'}) #find links to CSS files
        for css in css_files:
            css = url + css['href']
            self.LB1.insert(END, css) #add CSS links to LB1 listbox
            file = urllib2.URLopener()
            file.retrieve(css)
            print css #print CSS links to console (debug)

    def getJS(self):
        js_files = soup.findAll('script',{'src':True}) #find links to JS files and filter only the src attribute
        for js in js_files:
            if js['src'].startswith("//"): #check if relative or absolute URL to JS file
                js = js['src']
                self.LB1.insert(END, js) #add to LB1 listbox
                file = urllib2.URLopener() #open JS file for writing
                file.retrieve(js) #download JS file to disk
                print js #print JS links to console (debug)
            else:
                self.LB1.insert(END, js) #add links to LB1 listbox
                js = url + js['src']
                file = urllib2.URLopener() #open file for writing
                file.retrieve(js) #download JS file to disk
                print js #print JS links to console (debug)

    def getIMG(self):
        img_files = soup.findAll('img',{'src':True}) #find all links to images on page
        for img in img_files:
            if img['src'].startswith('http'): #check if img link is relative or absolute
                img = img['src']
                self.LB1.insert(END, img) #add img link to LB1 listbox
                file = urllib2.URLopener() #open file for writing
                file.retrieve(img) #save IMG to disk
                print img #print img links to console (debug)
            else:
                img = url + img['src']
                self.LB1.insert(END, img) #add to LB1 listbox
                file = urllib2.URLopener() #open file for writing
                file.retrieve(img) #download file to disk
                print img #print img links to console (debug)
        
app = siteRipper() #call main instance
app.mainloop() #call mainloop
