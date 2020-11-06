#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


muertes_df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                         '1mLx2L8nMaRZu0Sy4lyFniDewl6jDcgnxB_d0lHG-boc' +
                         '/export?gid=1456422453&format=csv', skiprows=1,
                         parse_dates=[0], na_values=['-'])
muertes_df['Fecha']=muertes_df['Fecha']+'/2020'
muertes_df['Fecha']=pd.to_datetime(muertes_df['Fecha'], format='%d/%m/%Y')


consolidado_df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                             '1mLx2L8nMaRZu0Sy4lyFniDewl6jDcgnxB_d0lHG-boc' +
                             '/export?gid=828979356&format=csv', skiprows=1,
                             parse_dates=[0], na_values=['-'])
consolidado_df.rename(columns={ consolidado_df.columns[0]: "Fecha" },
                      inplace=True)


hosp = consolidado_df.iloc[:, [0, 7, 8, 9, 10]].copy()
hosp = hosp.dropna()


hosp.columns = ['Fecha','cama_basica', 'cama_media', 'uti', 'uci']


hosp['cama_basica'] = hosp['cama_basica'].astype('int32')


hosp['hosp_total'] = (hosp.iloc[:,1].astype('int32') 
                 + hosp.iloc[:,2].astype('int32')
                 + hosp.iloc[:,3].astype('int32')
                 + hosp.iloc[:,4].astype('int32'))


fig, ax1 = plt.subplots(figsize=(7,5))
ax1.plot(muertes_df['Fecha'], muertes_df['Muertes COVID U07.1'], 
         color='blue', label='deaths')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(hosp['Fecha'], hosp['cama_basica'],
         color='orange', label='hospitalizations')
ax1.tick_params(axis='x', labelrotation=90 ) 
ax1.set_title('Deaths by COVID19 and Hospitalizations (regular beds)')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
ax1.set_xlabel("Time (days)")
ax1.set_ylabel(r"deaths")
ax2.set_ylabel(r"Hospitalizations")
fig.tight_layout()
fig.savefig('deaths_covid_raw.png')


muertes_df['Fecha'].min(), muertes_df['Fecha'].max()


hosp_muerte_df = muertes_df[['Fecha',
                             'Muertes COVID U07.1']].merge(hosp, 
                                                           on='Fecha', 
                                                           how='right')


hosp_muerte_df = hosp_muerte_df.resample('W-MON', on='Fecha').mean().reset_index()


fig, ax1 = plt.subplots(figsize=(7,5))
ax1.scatter(muertes_df['Fecha'], muertes_df['Muertes COVID U07.1'], s=3, 
                             facecolor='none', alpha=.3,color='blue')
ax1.plot(hosp_muerte_df['Fecha'], hosp_muerte_df['Muertes COVID U07.1'],
         color='blue', label='deaths')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(hosp_muerte_df['Fecha'], hosp_muerte_df['cama_basica'],
         color='orange', label='hospitalizations')
ax2.scatter(hosp['Fecha'], hosp['cama_basica'], 
            s=3, facecolor='none', alpha=.3, color='orange')
ax1.tick_params(axis='x', labelrotation=90 ) 
ax1.set_title('Deaths by COVID19 and Hospitalizations (regular beds)')
ax1.legend(loc='lower right')
ax2.legend(loc='upper right')
ax1.set_xlabel("Time (days)")
ax1.set_ylabel(r"deaths")
ax2.set_ylabel(r"Hospitalizations")
fig.tight_layout()
fig.savefig('deaths_covid_weekly_avg.png')


fig, ax = plt.subplots(figsize=(8,6))
ax.plot(hosp_muerte_df['cama_basica'], 
         hosp_muerte_df['Muertes COVID U07.1'], '.-k')

for i, txt in enumerate(hosp_muerte_df.index):
    test = str(hosp_muerte_df['Fecha'].iat[i])[5:10]
    ax.annotate(f'{test}', (hosp_muerte_df['cama_basica'].iat[i],
                            hosp_muerte_df['Muertes COVID U07.1'].iat[i]),
                xytext=(0, -15), 
                textcoords='offset points')
ax.set_ylabel('Average deaths per week')
ax.set_xlabel('Average hospitalizations per week')
ax.set_title('Connected scatterplot of deathsXhospitalizations (regular beds)')
fig.savefig('conn_scatter_regbeds.png')


fig, ax = plt.subplots(figsize=(8,6))
ax.plot(hosp_muerte_df['hosp_total'], 
         hosp_muerte_df['Muertes COVID U07.1'], '.-k')

for i, txt in enumerate(hosp_muerte_df.index):
    test = str(hosp_muerte_df['Fecha'].iat[i])[5:10]
    ax.annotate(f'{test}', (hosp_muerte_df['hosp_total'].iat[i],
                            hosp_muerte_df['Muertes COVID U07.1'].iat[i]),
                xytext=(0, -15), 
                textcoords='offset points')
ax.set_ylabel('Average deaths per week')
ax.set_xlabel('Average hospitalizations per week')
ax.set_title('Connected scatterplot of deathsXhospitalizations (all beds)')
fig.savefig('conn_scatter_allbeds.png')

