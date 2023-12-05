import pandas as pd
import pylab as plt  
import seaborn as sns
from unidecode import unidecode



def na_abs(df, ascend=False):
    df1 = df.isna().sum()
    df1=df1[df1!=0].sort_values(ascending = ascend)
    return df1

def na_perc(df, ascend=False):
    df1 = df.isna().mean()*100
    df1 = df1[df1!=0].sort_values(ascending = ascend)
    return df1

def na_absperc(df):
    return pd.concat([na_abs(df), na_perc(df)], axis=1, keys= ["abs_NA", "perc_NA"])


def categ_summ(df):
    '''
    Creates a modified version of 'describe objects' function
    
    Adds 3 new columns to evaluate the ratio between unique/level values
    and their frequency
    
    "resto_per" column may pinpoint potential misspelled errors as
    Top rows: indicate there are MANY LEVELS with very LOW FREQ
    Bottom rows:  indicate there is ONE LEVEL with EXCESIVE FREQ
    
    '''

    sumdf=df.describe(include=["object", "category"]).T
    sumdf["unicount_ratio"]=sumdf["unique"]/sumdf["count"]

    sumdf["resto_abs"]=(sumdf["count"]-sumdf["freq"])
    sumdf["resto_per"]=(sumdf["resto_abs"]*100)/sumdf["count"]

    sumdf.sort_values(["resto_per", "unique"])
    return sumdf



def variance_check(df, perc_a, perc_b):
    '''
    Creates a modified version of 'describe numeric' function
    
    Adds 2 new columns to dispay quantile A and B defined by the user
   
    NOTE: The function will only filter and evaluate the NUMERIC COLUMNS!
    perc_a and perc_b must be from 0-1
    '''
    subdf=df.select_dtypes(include='number')
    sumdf=subdf.describe(include="number").T

    sumdf["P" + str(int(perc_a*100))]=numeric_df.quantile(perc_a)
    sumdf["P" + str(int(perc_b*100))]=numeric_df.quantile(perc_b)

    return sumdf.sort_values("std", ascending = False)


def outliers(df):
    outliers = pd.DataFrame(columns=df.columns)
    stats=df.describe().transpose()
    stats['IQR'] = stats['75%'] - stats['25%']
    
    for col in stats.index:
        iqr = stats.at[col,'IQR']
        cutoff = iqr * 1.5
        lower = stats.at[col,'25%'] - cutoff
        upper = stats.at[col,'75%'] + cutoff
        results = df[(df[col] < lower) | 
                       (df[col] > upper)].copy()
        results['Outlier'] = col
        outliers = outliers.append(results)
    return outliers



def reduc_mem(df):
    '''
    reduce the memory usage of the dataframe by:
    1),2) downcasting the int and float columns into numeric with lowest bits possible
    3) collapsing object columns into cateory (factor levels)
    
    '''
    dytpes_list=df.dtypes

    for i in range(len(dytpes_list)):
        if dytpes_list[i]=="int" :
            df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], downcast='integer')
        elif dytpes_list[i]=="float" :
            df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], downcast='float')
        elif dytpes_list[i]=="object" :
            df[df.columns[i]] = df[df.columns[i]].astype('category')
        else:
            pass
    return df

def na_heatmap(df: pd.DataFrame) -> None:  
    """
    NA'S HEATMAP
    """
    plt.figure(figsize=(10, 6)) # 100x60 pixeles
    sns.heatmap(df.isna(),          # datos
                yticklabels=False,  # quita las etiquetas del eje y
                cmap='rainbow',     # mapa de color
                cbar=False,         # sin barra lateral
               )
    plt.show();

def colnnam_clean(df):
    '''
    Modify annoying naming
    Ad-hoc function to deal with specific dataframes
    '''
    colnams=df.columns
    cols_list=[]
    for i in colnams:
        j=i.replace(" ", "_").lower()
        j=j.replace(":", "_")
        j=j.replace(".", "_")
        
        j=j.replace("(", "")
        j=j.replace(")", "")
        
        j=j.replace("/", "_")
        
        j=j.replace("__", "_")

        j=unidecode(j)  
        
        if j[-1]=="_":
            j=j[:-2]
            
        elif j[0]=="_":
            j=j[1:]
            
        cols_list.append(j)
    df.columns=cols_list
        
    return df


def namvector_clean(list_vec):
    '''
    Modify annoying naming
    Ad-hoc function to deal with specific dataframes
    '''
    
    list_vec2=[]
    for i in list_vec:
        j=i.replace(" ", "_").lower()
        j=j.replace(":", "_")
        j=j.replace(".", "_")
        
        j=j.replace("(", "")
        j=j.replace(")", "")
        
        j=j.replace("/", "_")
        
        j=j.replace("__", "_")

        j=unidecode(j)
        
        if j[-1]=="_":
            j=j[:-2]
            
        elif j[0]=="_":
            j=j[1:]
            
        list_vec2.append(j)
    
    return list_vec2


def DF_wo_colX(df, colnameX_list):
    '''
    fuction to work or make evals with a dataframe without a certain column
    e.g., filter out index_id to eval true duplicates
        
    example of input type:
        colnameX_list=["actor_id"]
        colnameX_list=["actor_id", "last_update"]
        ...
    
    '''
    df1=df.loc[:, ~df.columns.isin(colnameX_list)]
    return df1



'''

USEFULL CODE STRUCTURE (NON-FUNCTIONS)



'''
