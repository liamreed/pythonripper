import urllib2 #urllib2 required for fetching information from ripURL
import requests #for downloading files
import os #for directory path
from PIL import Image
import time #delay actions so it doesnt freeze
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
        self.chosenPath = self.E2.get() #get path from Entry 2
        if self.ripURL != "": #check if ripURL is empty
            self.getHTML() #get HTML source of page
            self.getCSS() #get full CSS urls from page
            self.getJS() #get full JS urls from page
            self.getIMG() #get full IMG urls from page
        else:
            errortext = "URL field was empty"
            self.L3.config(text= "URL field was empty") #report error to user via L3 label
            print errortext

    def create_interface(self):
        self.geometry("950x580+150+150") #set size of window
        L1 = tk.Label(text="URL to rip")
        L1.place(x=2, y=4, anchor="nw")
        L2 = tk.Label(text="Output Directory")
        L2.place(x=2, y=26)
        self.L3 = tk.Label() #error message label
        self.L3.place(x=475, y=547)
        self.E1 = tk.Entry(self, width=135) #URL input field
        self.E1.place(x=120, y=6)
        self.E2 = tk.Entry(self, width=130) #Directory path field
        self.E2.place(x=150, y=30)
        self.LB1 = tk.Listbox(self, width=135, height=30)
        self.LB1.place(x=120, y=52)
        self.chosenPath = './'
        B1 = tk.Button(self, text="Dir", command=self.saveDialog) #Dir button fires saveDialog method
        B1.place(x=120, y=26)
        B2 = tk.Button(self, text="Download", command=self.doRip) #Download button fires doRip method
        B2.place(x=870, y=540)
        
    def saveDialog(self):
        self.chosenPath = tkFileDialog.askdirectory(initialdir='.')
        print self.chosenPath
        self.E2.insert(0, self.chosenPath)

    def getHTML(self):
        print self.ripURL
        print type(self.ripURL)
        site = urllib2.urlopen(self.ripURL) #open URL inputted in E1 Entry
        data = site.read()
        self.soup = BeautifulSoup(data)
        if not os.path.exists(self.chosenPath):
            os.makedirs(self.chosenPath)
        print self.chosenPath + "/source.txt"
        file = open(self.chosenPath + '/source.txt', 'w')
        file.writelines(data) #save HTML source to disk
        file.close()
        time.sleep(0.4)
        print "Saved page source to disk - source.txt" #print complete message to console

    def getCSS(self):
        print "Starting Asset Rip... [May become unresponsive]" #Give user feedback on process
        css_files = self.soup.findAll('link',{'rel':'stylesheet'}) #find urls to CSS files
        for css in css_files:
            if css['href'].startswith("//"):
                css = css['href'].replace('//', 'http://')
                self.LB1.insert(tk.END, css) #add CSS urls to LB1 listbox
                print css #print CSS urls to console (debug)
                url = css
                self.downloadFile(url, path= self.chosenPath + '/css/')
                time.sleep(0.1)
            elif css['href'].startswith("http"):
                css = css['href']
                self.LB1.insert(tk.END, css) #add CSS urls to LB1 listbox
                print css #print CSS urls to console (debug)
                url = css
                self.downloadFile(url, path= self.chosenPath + '/css/')
                time.sleep(0.1)
            else:
                css = self.ripURL + css['href']
                self.LB1.insert(tk.END, css) #add CSS urls to LB1 listbox
                print css #print CSS urls to console (debug)
                url = css
                self.downloadFile(url, path= self.chosenPath + '/css/')
                time.sleep(0.1)

    def getJS(self):
        js_files = self.soup.findAll('script',{'src':True}) #find urls to JS files and filter only the src attribute
        for js in js_files:
            if js['src'].startswith("//"): #check if relative or absolute URL to JS file
                js = js['src'].replace('//', 'http://')
                self.LB1.insert(tk.END, js) #add to LB1 listbox
                print js #print JS urls to console (debug)
                url = js
                self.downloadFile(url, path= self.chosenPath + '/js/')
                time.sleep(0.1)
            else:
                self.LB1.insert(tk.END, js) #add urls to LB1 listbox
                js = self.ripURL + js['src']
                print js #print JS urls to console (debug)
                url = js
                self.downloadFile(url, path= self.chosenPath + '/js/')
                time.sleep(0.1)

    def getIMG(self):
        img_files = self.soup.findAll('img',{'src':True}) #find all urls to images on page
        for img in img_files:
            if img['src'].startswith('http'): #check if img url is relative or absolute
                img = img['src']
                self.LB1.insert(tk.END, img) #add img url to LB1 listbox
                print img #print img urls to console (debug)
                url = img
                self.downloadFile(url, path= self.chosenPath + '/img/')
                time.sleep(0.1)
            elif img['src'].startswith('//'): #check if img url is relative or absolute
                img = img['src'].replace('//', 'http://')
                self.LB1.insert(tk.END, img) #add img url to LB1 listbox
                print img #print img urls to console (debug)
                url = img
                self.downloadFile(url, path= self.chosenPath + '/img/')
                time.sleep(0.1)
            else:
                img = self.ripURL + img['src']
                self.LB1.insert(tk.END, img) #add to LB1 listbox
                print img #print img urls to console (debug)
                url = img
                self.downloadFile(url, path= self.chosenPath + '/img/')
                time.sleep(0.1)

    def createFilename(self, url, name, path):
        dotSplit = url.split('.')
        if not os.path.exists(path):
            os.makedirs(path)
        if name == None:
            # use the same as the url
            slashSplit = dotSplit[-2].split('/')
            name = slashSplit[-1]
        ext = dotSplit[-1]
        file = '{}{}.{}'.format(path, name, ext)
        return file

    def downloadFile(self, url, name=None, path='./'):
        file = self.createFilename(url, name, path)
        with open(file, 'wb') as f:
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)

app = siteRipper() #call main instance
app.mainloop() #call mainloop
