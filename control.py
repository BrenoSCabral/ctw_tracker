from get_data import get_data
from filt_data import filt_data

def main():
    ids = {'Rio Grande 2 (RS)' : '303',
     'Tramandaí (RS)' : '305',
     'Pontal do Sul (PR)' : '398',
     'Paranaguá (PR)' : '300',
     'Antonina (PR)' : '397',
     'Ilhabela (SP)' : '309',
     'DHN (RJ)' : '304',
     'Tamandaré (PE)': '399',
     'Pecém (CE)' : '307',
     'Ribamar (MA)' : '302'}
    
    for name, id in ids.items:
        try:
            get_data(id)
        except Exception as e:
            print(f'Problem getting the data --- {name} ---')
            print(e)
    
        try:
            filt_data(id)
        except Exception as e:
            print(f'Problem filtering the data --- {name} ---')
            print(e)