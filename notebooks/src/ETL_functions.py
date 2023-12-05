###

def prod_clean_amz1(prod_list, keys):    
    '''
    Keep elements that contain "€"" as it indicates they actually refer to a product
    Discard str lines including words (in ´keys_discard´) as it indicates they are irrelevant
    
    '''
    prod_list1=[]
    
    for theprod in prod_list:
        
        # if contains a price, it is a product, so continue!
        if "€" in "".join(theprod): 
            
            # eval if the str contains non-relevant info (keys_discard)    
            theprod1=[]
            for i in theprod:
                T=0
                # if the product element is to discard, > 0 
                T=sum((j in i) * 1 for j in keys) 
                
                # if the product element == 0 keep it for the moment
                if T == 0:
                    theprod1.append(i)
                else:
                    pass
                
            prod_list1.append(theprod1)
            
    return prod_list1

####

def complete_price_amz1(prod_list):
    '''
    sometimes the price get split by the comma.
    Eval if that is the case and correct it by joining the int value iof the index before
    
    '''
    prod_list1=[]
    for product in prod_list:
        
        # confirm the index of the price
        res=0
        for j in range(len(product)): 
            
            if ("Antes" in product[j]):
                product[j]=product[j].replace("€", "HAHAHA")
            
            
            
            if (("€" in product[j]) and ("Antes" in product[j])==False):
                res=j
                
        # if it includes € and , --> theprice is complete 
        if([("€" in t)*1 for t in product] == [("," in t)*1 for t in product]):
            #pass
            product[res]= product[res].replace(",", ".")
        
        # if it includes € but not , --> theprice is incomplete , paste the previous number
        else:
            ress= product[res-1] + "." + product[res]
            product[res]=ress
    
        prod_list1.append(product)
    
    
    return prod_list1

###


def relev_inf_amz1(product_list, color_val): # list with elements
    '''
    Take out float data referring to score rate and splited price
    Add a new column to register the color
    
    '''
    product_list1=[] # new list for containing cleaned elements
    for product in product_list:  # for each element containing values
        clean_prod=[] # new object for containing values of the cleaned element
        for prods in product: # for each value
            try:
                float(prods)
            except ValueError:
                if (prods != "Marca Amazon"):
                    clean_prod.append(prods) # if not floatable, keep it

        clean_prod = clean_prod + [color_val] #when the loop ends, add the color value
        
        product_list1.append(clean_prod) #add the cleaned elemnt to the list
    return product_list1






