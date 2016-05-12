#Patagonia Sales Notifier 
from urllib import request

class patagoniaSale:
    max_percent = 0.0
    max_percent_item = ""
    url_list = []
    items = {}
    base_url = "";
    num_of_pages = 0;
    desired_percent_off = 50

    #Constructor
    def __init__(self, url):
      self.base_url = url
      self.url_list.append(url)
      self.desired_percent_off = input("Enter a desired percent off: ")

    #EFFECTS: stores number of pages we need to look at
    def number_of_pages(self):
        r = request.urlopen(self.base_url)
        bytecode = r.read()
        htmlstr = bytecode.decode()
        findme = '''<span>of</span> <span style="padding:0 2px;">'''
        self.num_of_pages = int(htmlstr[int(htmlstr.find(findme)+45)])

    #EFFECTS: insert all url that we need to look at
    def insertallurls(self):
        counter = 0
        template = "http://www.patagonia.com/us/shop/web-specials-mens?k=1D-ga&ps="
        while counter < self.num_of_pages - 1:
            index = counter + 2
            new_url = template + str(index)
            self.url_list.append(new_url)
            counter = counter + 1

    #EFFECTS: stores all itesm descriptsion and percetnage of discount
    def get_items_and_percentages(self, URL):
        url = request.urlopen(URL) #Reading in URL
        code = url.read()
        htmlstring = code.decode()
        start = 0
        while(htmlstring.find(''' data-benefitstatement=''',start) != -1):
            #getting the item description
            number1 = htmlstring.find(" data-benefitstatement=", start)
            s1 = " data-benefitstatement="
            number2 = htmlstring.find('''"> <strong><a data-current-color=''', start)
            len(s1)
            item_description = htmlstring[number1 + len(s1) + 1:number2]
        
            #getting the original price of item
            number3 = htmlstring.find('''</a></strong> <span style="display:block"><del>$''',start)
            s2 = '''</a></strong> <span style="display:block"><del>$'''
            number4 = htmlstring.find('''</del>&nbsp;<span><strong>$''',start)
            s3 = '''</del>&nbsp;<span><strong>$'''
            orginal_price = htmlstring[number3 + len(s2):number4]

            number5 = htmlstring.find('''</strong></span></span> <div class="checkbox ''',number4)
            final_price = htmlstring[number4 + len(s3):number5]

            percent = (1 - (float(final_price)/float(orginal_price))) * 100
            self.items[item_description] = percent
            if self.max_percent < percent:
                self.max_percent = percent
                self.max_percent_item = item_description
        
            start = number5
            
    #EFFECTS: iterate through every result
    def every_page(self):
        index = 0
        while (index < self.num_of_pages):
            self.get_items_and_percentages(self.url_list[index])
            index = index + 1

    #EFFECTS: print the list of items that matches the criteria
    def print_item(self):
        for item in self.items:
            if self.items[item] >= float(self.desired_percent_off):
                print("Item description: " + item)
                print("*****************************")
                print("Percent sale: " + str(self.items[item]))
                print("***************************** \n")


    #EFFECTS: print out result
    def result(self):
        self.number_of_pages()
        self.insertallurls()
        self.every_page()
        if self.max_percent >= float(self.desired_percent_off):
            statement = "You got lucky! Patagonia is having websale where at least one item is more than " +  self.desired_percent_off +" percent off!"
            print(statement)
            print("These items are ******************************\n")
            self.print_item()
        else:
            statement = "Sorry! Patagonia is not having wesale where every item is below " + self.desired_percent_off + " percent off"
            print(statement)
            
#main
NewSale = patagoniaSale("http://www.patagonia.com/us/shop/web-specials-mens?k=1D-ga")
print("Checking if there is a good deal at patagonia.com.....")
NewSale.result()






