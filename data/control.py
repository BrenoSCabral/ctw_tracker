from get_data import get_data
import filt_data as filt
import unicodedata
import plotly.express as px


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


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
    
    for name, id in ids.items():
        try:
            data = get_data(id)
        except Exception as e:
            print(f'Problem getting the data --- {name} ---')
            print(e)
    
        try:
            filtered_data = filt.filter_data(data)
            filtered_data['station'] = name
            filtered_data.index.name = 'Date (UTC Time)'

            fig = px.line(filtered_data, x=filtered_data.index, 
                          y='filt', title=f'CTW monitor - {name}',
                          labels={
                            'filt': 'Sea Surface Height (cm)',
                            'index': 'UTC Time'
                        })
            filename = remove_accents(name.lower().replace(' ', '_')[:-5])
            fig.write_html(f"graphs/{filename}.html")



        except Exception as e:
            print(f'Problem filtering the data --- {name} ---')
            print(e)

if __name__ == '__main__':
    main()