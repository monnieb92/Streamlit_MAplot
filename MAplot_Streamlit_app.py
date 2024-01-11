#!/bin/python 

import pandas as pd
from PIL import Image
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import StringIO
import matplotlib.pyplot as plt

uploaded_file = st.sidebar.file_uploader("Upload your input txt file", type=["txt"])
st.write('This is the path to the txt file for the differential analysis', uploaded_file)
filename_csv=st.text_area('The filename for the csv file, must end in .csv',value='Differential_Analysis.csv')
adjp = st.number_input('adjusted p-value', value=0.05)
st.write('The current adjusted p-value is ', adjp)
filename_png=st.text_area('The filename for the MA plot, must end in .png',value='MAplot.png')
filename_html=st.text_area('The html name for the MA plot, must end in .html',value='MAplothtml.html')
foldchangeup = st.number_input('Fold Change Up', value=1.5)
st.write('The current Fold Change for up regulated is ', foldchangeup)

foldchangedn = st.number_input('Fold Change Down', value=1.5)
st.write('The current Fold Change for down regulated is ', foldchangedn)

padj_column=st.text_area('The name of the column containing the adjusted p-values',value='padj')

l2FChg_column=st.text_area('The name of the column containing the log2fold Change values',value='log2FoldChange')
maplot_title=st.text_area('The title of the MA plot',value='Differential Analysis')
dot_names=st.text_area('The names you can select on the MA plot',value='seqnames')
titlesize_font=st.number_input('The font size of the Title',value=15)
yax_min=st.number_input('The minimun value of yaxis',value=-8)
yax_max=st.number_input('The maximum value of yaxis',value=8)
yax_font=st.number_input('The y-axis title font size',value=12)
yax_tick_font=st.number_input('The y-axis tick font size',value=10)
xax_font=st.number_input('The x-axis title font size',value=12)
xax_tick_font=st.number_input('The x-axis tick font size',value=10)
sizeofmarker=st.number_input('The dot size',value=2)
figure_width=st.number_input('The width of the figure',value=500)
figure_height=st.number_input('The height of the figure',value=500)
xax_tick_range_max=st.number_input('The x-axis tick range max number if not log transforming baseMean',value=6)
st.write('The 6 tick values added when not log transforming baseMean are: tickvals=[0, 1, 10, 100, 1000, 10000,100000,1000000]')
fontnames=st.text_area('The name of the fonts, Arial or Arial Black',value='Arial Black')
logchoice=st.selectbox("Pick a choice for the transformation of the baseMean", ["log2", "log10", "None"])
# Correct GitHub raw CSV file URL
github_file_url = 'https://raw.githubusercontent.com/monnieb92/Streamlit_MAplot/main/GSE160468_resultCTCFq0.01BLfiltered_SMARCA5dTAG47_24hrvs0hr.normTC_Kasumi1.txt'

# Button click to determine differential analysis
if st.button('Determine Differential analysis'):
    if uploaded_file is not None:
        upload_file_df = pd.read_csv(uploaded_file, sep="\t")
    else:
        response = requests.get(github_file_url)
        upload_file_df = pd.read_csv(StringIO(response.text), sep="\t")
    #First drop any NAs that are within the baseMean
    result_table = upload_file_df.dropna(subset=['baseMean'])
    # Replace NA values with 1
    result_table = result_table.fillna(1)

    # Calculate FoldChange column
    result_table['FoldChange'] = (2 ** (np.abs((result_table['log2FoldChange']))) * np.sign(result_table['log2FoldChange']))
    result_table = (result_table.assign(
        category=np.where((result_table['padj'] <= adjp) & (result_table['FoldChange'] <= -foldchangedn), "Down", 
                          np.where((result_table['padj'] <= adjp) & (result_table['FoldChange'] >= foldchangeup), "Up", "NS"))
    ))
    category_counts = result_table['category'].value_counts()
    st.write('Category Counts:')
    st.write(category_counts)
    result_table_df = result_table
    # Save result_table as a CSV file
    result_table_csv = result_table.to_csv(index=False)
    st.download_button('Download Result Table CSV',data=result_table_csv, file_name=filename_csv)
   
    fig = px.scatter(result_table_df,
        x=np.log2(result_table_df['baseMean']) if logchoice == 'log2' else np.log10(result_table_df['baseMean']) if logchoice == 'log10' else result_table_df['baseMean'],
        y='log2FoldChange',
        color='category',
        hover_name=dot_names,
        color_discrete_map={'Up': '#ca0020', 'NS': '#bababa', 'Down': '#0571b0'},
        opacity=1,
        title=maplot_title)

    fig.update_traces(marker_size=sizeofmarker)
    # Add horizontal line at y = 0
if logchoice == 'log2':
    minxaxis = np.log2(result_table_df['baseMean']).min() 
    if logchoice == 'log10': 
        minxaxis = np.log10(result_table_df['baseMean']).min() 
    else: 
        minxaxis = result_table_df['baseMean'].min()
    fig.add_shape(  go.layout.Shape(type="line",
         xref="paper",
         x0=minxaxis,
         x1=1,
         y0=0,
         y1=0,
         line=dict(color="black", width=1),
         ))
        # Set log scale for x-axis
    if logchoice == 'None':
        fig.update_xaxes(type="log",showgrid=False,
                ticks="outside", tickvals=[0, 1, 10, 100, 1000, 10000,100000,1000000],
                dtick=1,range=[-1,xax_tick_range_max])
    else:
        fig.update_layout(xaxis=dict(showgrid=False))

        # Set y-axis limits and ticks
    fig.update_yaxes(ticks="outside", tickvals=list(range(yax_min, (yax_max+1),2)), range=[yax_min, yax_max],dtick=2,showgrid=False)


        # Update layout settings
    fig.update_layout(showlegend=True,
            xaxis_title="log2(Base Mean)" if logchoice == 'log2' else "log10(Base Mean)" if logchoice == 'log10' else "Base Mean",
            yaxis_title="log2 Fold Change",
            width=figure_width,
            height=figure_height,
            plot_bgcolor='white',
            legend_title_text="Category",
            title_x=0.4,
            title_font=dict(family=fontnames,color='black',size=titlesize_font))
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',
                 ticks="outside",tickson="boundaries",ticklen=5,tickcolor="black",
                 tickfont=dict(family=fontnames,color='black',size=xax_tick_font),
                 title_font=dict(family=fontnames,color='black',size=xax_font))

    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',
                 ticks="outside",tickson="boundaries",ticklen=5,tickcolor="black",
                 tickfont=dict(family=fontnames,color='black',size=xax_tick_font),
                 title_font=dict(family=fontnames,color='black',size=yax_font))


        # Show the plot
    fig.write_image('MAplot.png',scale=2)
    st.plotly_chart(fig)
    
    save=st.download_button('PNG file name to save', data=open('MAplot.png','rb').read(), file_name=filename_png)
    
    plot_html = fig.to_html()
    save=st.download_button('html file name to save', data=plot_html, file_name=filename_html,mime='text/html',)
