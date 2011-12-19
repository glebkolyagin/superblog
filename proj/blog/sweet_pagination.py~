import math

class MyPage:
    def __init__(self,h,n):
        self.href=int(h)
        self.name=n       

#cool paginator 
#attirbutes: django.core.paginator.Paginator paginator        
#int pages_show - how many pages you want to show 
#int p - current page
#return list of MyPage instances
#using in view: {% for p in page_list %}<a href="/?{{ p.href }}">{{ p.name }}&nbsp;</a>{% endfor %}
#will show smth like 1 ... 6 7 8 9 10 or 1 ... 4 5 6 ... 10 or 1 2 3 4 5 ... 10
def get_page_list(paginator,pages_show,p):
    page_list=[]
    p=int(p);
    count_page=paginator.num_pages
    
    if pages_show<5:
        raise ValueError("Quantity of pages should be equal or more than 5");
    if count_page>pages_show:
        if p<pages_show-1:    
            for i in range(1,pages_show-1):
                page_list.append(MyPage(i,i))
            page_list.append(MyPage(pages_show-1,'...'))                    
            page_list.append(MyPage(count_page,count_page))
        elif p>count_page-(pages_show-2):  
            page_list.append(MyPage(1,1))
            page_list.append(MyPage(count_page-pages_show+2,'...'))
            for i in range(count_page-(pages_show-3),count_page+1):
                page_list.append(MyPage(i,i))
        else:
            page_list.append(MyPage(1,1))
            page_list.append(MyPage(p-int(float(pages_show-4)/float(2))-1,'...'))
            for i in range(p-int(float(pages_show-4)/float(2)),int(p+math.ceil(float(pages_show-4)/float(2)))):
                    page_list.append(MyPage(i,i))
            page_list.append(MyPage(p+math.ceil(float(pages_show-4)/float(2)),'...'))
            page_list.append(MyPage(count_page,count_page))
    elif count_page>1:
        for i in range(1,count_page+1):
            page_list.append(MyPage(i,i))

    return page_list
