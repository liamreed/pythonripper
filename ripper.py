import urllib2 #urllib2 required for fetching information from ripURL
import urllib
import mtTkinter as tk #import mtTkinter for GUI components
import tkFileDialog #import tkFileDialog for Open Directory window
from BeautifulSoup import * #import BeautifulSoup library for HTML scraping
       
class siteRipper(tk.Tk): #init window
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Site Ripper")
        self.create_interface() #init GUI widgets
        self.resizable(0,0) #non-resizable

    def doRip(self):
        self.LB1.delete(0, tk.END)
        self.ripURL = self.E1.get() #get text from Entry 1
        if self.ripURL != None: #check if ripURL is empty
            self.getHTML() #get HTML source of page
            self.getCSS() #get full CSS links from page
            self.getJS() #get full JS links from page
            self.getIMG() #get full IMG links from page
        else:
            self.L3.text = "URL field was empty" #report error to user via L3 label

    def create_interface(self):
        self.geometry("650x250+150+150") #set size of window
        L1 = tk.Label(text="URL to rip")
        L1.place(x=2, y=4, anchor="nw")
        L2 = tk.Label(text="Output Directory")
        L2.place(x=2, y=26)
        self.L3 = tk.Label() #error message label
        self.L3.place(x=140, y=210)
        self.E1 = tk.Entry(self, width=85) #URL input field
        self.E1.place(x=120, y=6)
        self.E2 = tk.Entry(self, width=80) #Directory path field
        self.E2.place(x=150, y=30)
        self.LB1 = tk.Listbox(self, width=85)
        self.LB1.place(x=120, y=52)
        B1 = tk.Button(self, text="Dir", command=self.saveDialog) #Dir button fires saveDialog method
        B1.place(x=120, y=26)
        B2 = tk.Button(self, text="Download", command=self.doRip) #Download button fires doRip method
        B2.place(x=570, y=220)
        
    def saveDialog(self):
        path = tkFileDialog.askdirectory()
        self.E1.text = path
        return path

    def getHTML(self):
        print self.ripURL
        print type(self.ripURL)
        site = urllib2.urlopen(self.ripURL) #open URL inputted in E1 Entry
        data = site.read()
        self.soup = BeautifulSoup(data)
        file = open('source.txt', 'w')
        file.writelines(data) #save HTML source to disk
        file.close()
        print data #print HTML to console (debug)

    def getCSS(self):
        css_files = self.soup.findAll('link',{'rel':'stylesheet'}) #find links to CSS files
        for css in css_files:
            css = self.ripURL + css['href']
            self.LB1.insert(tk.END, css) #add CSS links to LB1 listbox
            print css #print CSS links to console (debug)
            link = css
            self.downloadFile(link)

    def getJS(self):
        js_files = self.soup.findAll('script',{'src':True}) #find links to JS files and filter only the src attribute
        for js in js_files:
            if js['src'].startswith("//"): #check if relative or absolute URL to JS file
                js = js['src']
                self.LB1.insert(tk.END, js) #add to LB1 listbox
                print js #print JS links to console (debug)
                link = js
                self.downloadFile(link)
            else:
                self.LB1.insert(tk.END, js) #add links to LB1 listbox
                js = self.ripURL + js['src']
                print js #print JS links to console (debug)
                link = js
                self.downloadFile(link)

    def getIMG(self):
        img_files = self.soup.findAll('img',{'src':True}) #find all links to images on page
        for img in img_files:
            if img['src'].startswith('http'): #check if img link is relative or absolute
                img = img['src']
                self.LB1.insert(tk.END, img) #add img link to LB1 listbox
                print img #print img links to console (debug)
                link = img
                self.downloadFile(link)
            else:
                img = self.ripURL + img['src']
                self.LB1.insert(tk.END, img) #add to LB1 listbox
                print img #print img links to console (debug)
                link = img
                self.downloadFile(link)

    def downloadFile(self, link):
        try:
            self.currentFile = urllib.urlretrieve(link)
        except:
            self.L3.text = "Error downloading file"

app = siteRipper() #call main instance
app.mainloop() #call mainloop
