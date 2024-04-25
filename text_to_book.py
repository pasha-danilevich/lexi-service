import os


path = 'C:\\Users\\Pavel\\Desktop\\'
file_name = 'book.txt'
file_path = path + file_name
page_size = 2000

book = []     

def get_page(file):
    file_page_size = 0 
    page = []
    
    while file_page_size < page_size:
        line = file.readline()
        if line == '\n':
            continue
        
        if not line:
            return (page, True)
        
        if len(line) < 25:
            file_page_size += 100
        else:
            file_page_size += len(line)
            
        page.append(line)
        
    else:  
        return (page, False)
    
        
with open(file_path, 'r') as file:

    while True:
        page, is_end = get_page(file)
        book.append(page)
        if is_end:
            break
        
        

    



# i = 1
# for page in book:
#     print(f'{i}: {page[0][:30]}')
#     i += 1
    
for page in book:
    
    print(*page)
    print('--------------------')