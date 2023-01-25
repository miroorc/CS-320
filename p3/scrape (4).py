# project: p3
# submitter: mchoi82
# partner: none
# hours: 24
import pandas as pd
import scrape
import requests
import time

def reveal_secrets(driver, url, travellog):
    
    clue_lst = travellog['clue'].values.tolist()     
    clue_val = ''.join(str(i) for i in clue_lst)
    
    driver.get(url)
    text = driver.find_element("id","password").send_keys(clue_val)
    btn = driver.find_element('id','attempt-button')
    
    btn.click()
    time.sleep(2)
    
    btnn = driver.find_element('id', 'securityBtn')
    btnn.click()
    time.sleep(3)
    
    pic = driver.find_element('id', 'image')
    adr = pic.get_attribute('src')
    req = requests.get(adr)
    f = open('Current_Location.jpg', 'wb')
    result = f.write(req.content)
    f.close()
    
    
    location = driver.find_element("tag name","p")
    bascom = location.text
    return bascom   

    
    
        

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []
        self.children = ''


    def dfs_search(self, node):
        self.visited.clear()
        self.order.clear()
        return self.dfs_visit(node)

    def dfs_visit(self, node):
        if node in self.visited:
            return
        self.visited.add(node)
        self.children = self.visit_and_get_children(node)
        
        for elem in self.children:
            self.dfs_visit(elem)
            
    def bfs_search(self, node):
        todo = [node]
        added = {self}
    
        while len(todo) > 0:
            curr_node = todo.pop(0)
            self.children = self.visit_and_get_children(curr_node)
            added.add(curr_node)
            
            for elem in self.children:
                if not (elem in added):
                    if not elem in todo:
                        todo.append(elem)

            

            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        self.order.append(node)
        children = []
        for char, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(char)
        return children            

        


class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
        self.final_str = ''
        
    def visit_and_get_children(self, file):
        with open(f"file_nodes/{file}", "r") as file:
            var = file.readlines()
            node = var[0].strip()
            child = var[1].strip()
            print('node:', node, 'child:',child)
            var[1] = child.split(',')
            children = var[1]
        self.order.append(node[0])
        self.final_str = ''.join(self.order)
        return children
    
    def concat_order(self):
        return self.final_str


class WebSearcher(GraphSearcher):
    def __init__(self, webdriver):
        super().__init__()
        self.tble = pd.DataFrame()
        self.url = None
        self.href = []
        self.webdriver = webdriver

    def visit_and_get_children(self, url):
        df = pd.DataFrame()
        #self.href = []
        self.webdriver.get(url)
        for var in self.webdriver.find_elements('tag name', 'a'):
            self.href.append(var.get_attribute('href'))
        self.order.append(url)
        df = pd.read_html(url)
        self.tble = pd.concat([self.tble, df[0]], ignore_index = True)
        return self.href
   
    
    def table(self):
        return self.tble
   









