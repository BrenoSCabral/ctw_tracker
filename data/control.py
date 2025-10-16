'''
TODO:

Cortar a serie and eu tiver descontinuidade de dado
Pegar toda a serie temporal dos instrumentos, mas focar o display nos dois últimos meses somente
Criar uma Navbar
'''

from get_data import get_data
from process_data import process_data as proc_data
import unicodedata
import plotly.graph_objects as go
import datetime
from datetime import timedelta


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
            filtered_data = proc_data(data)


            fig = go.Figure()
            for seg in filtered_data:
                seg['station'] = name
                seg.index = seg.index.normalize()
                seg.index.name = 'Date (UTC Time)'

                fig.add_trace(go.Scatter(
                x=seg.index,
                y=seg['filt'],
                mode='lines',
                line=dict(color='royalblue', width=2),
                showlegend=False, # não mostra na legenda,
                name='',
                hovertemplate=(
                    '<b>Date</b> %{x}<br>' +
                    '<b>Sea Surface Height (cm):</b> %{y:.2f}<extra></extra>'
                )
                ))

            # fig.update_layout(
            #     xaxis=dict(fixedrange=False),
            #     yaxis=dict(fixedrange=True)
            # )


            end_date = datetime.datetime.now() - datetime.timedelta(hours=3)
            start_date = end_date - datetime.timedelta(days=60)

            fig.update_layout(
                title=f'CTW monitor - {name}',
                xaxis_title='Date (UTC Time)',
                yaxis_title='Sea Surface Height (cm)',
                template='plotly_white'
            )
            fig.update_xaxes(range=[start_date, end_date])
    


            filename = remove_accents(name.lower().replace(' ', '_')[:-5])
            fig.write_html(f"../graphs/{filename}.html")



        except Exception as e:
            print(f'Problem filtering the data --- {name} ---')
            print(e)

if __name__ == '__main__':
    main()