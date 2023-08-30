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

adjp = st.number_input('adjusted p-value', value=0.05)
st.write('The current adjusted p-value is ', adjp)

foldchangeup = st.number_input('Fold Change Up', value=1.5)
st.write('The current Fold Change for up regulated is ', foldchangeup)

foldchangedn = st.number_input('Fold Change Down', value=1.5)
st.write('The current Fold Change for down regulated is ', foldchangedn)

padj_column=st.text_area('The name of the column containing the adjusted p-values',value='padj')

l2FChg_column=st.text_area('The name of the column containing the log2fold Change values',value='log2FoldChange')
maplot_title=st.text_area('The title of the MA plot',value='Differential Analysis')
titlesize_font=st.number_input('The font size of the Title',value=15)
yax_min=st.number_input('The minimun value of yaxis',value=-8)
yax_max=st.number_input('The maximum value of yaxis',value=8)
yax_font=st.number_input('The y-axis title font size',value=12)
yax_tick_font=st.number_input('The y-axis tick font size',value=10)
xax_font=st.number_input('The x-axis title font size',value=12)
xax_tick_font=st.number_input('The x-axis tick font size',value=10)
figure_width=st.number_input('The width of the figure',value=450)
figure_height=st.number_input('The height of the figure',value=500)

# Correct GitHub raw CSV file URL
github_file_url = 'https://raw.githubusercontent.com/monnieb92/Streamlit_MAplot/main/GSE160468_resultCTCFq0.01BLfiltered_SMARCA5dTAG47_24hrvs0hr.normTC_Kasumi1.txt'

# Button click to determine differential analysis
if st.button('Determine Differential analysis'):
    if uploaded_file is not None:
        upload_file_df = pd.read_csv(uploaded_file, sep="\t")
    else:
        response = requests.get(github_file_url)
        upload_file_df = pd.read_csv(StringIO(response.text), sep="\t")
    # Replace NA values with 1
    result_table = upload_file_df.fillna(1)

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
    st.download_button('Download Result Table CSV',data=result_table_csv, file_name='result_table.csv')
   
    fig = px.scatter(result_table_df,
        x='baseMean',
        y='log2FoldChange',
        color='category',
        color_discrete_map={'Up': '#ca0020', 'NS': '#bababa', 'Down': '#0571b0'},
        opacity=0.6,
        title=maplot_title)

     # Add horizontal line at y = 0
    fig.add_shape(  go.layout.Shape(type="line", x0=min(result_table_df['baseMean']),
         x1=max(result_table_df['baseMean']),
         y0=0,
         y1=0,
         line=dict(color="black", width=1),
         ))
        # Set log scale for x-axis
    fig.update_xaxes(type="log")

        # Set y-axis limits and ticks
    fig.update_yaxes(ticks="outside", tickvals=list(range(yax_min, (yax_max+1),2)), range=[yax_min, yax_max],dtick=2,showgrid=False)

        # Set x-axis ticks for log scale
    fig.update_xaxes(ticks="outside", tickvals=[10, 100, 1000, 10000],showgrid=False)

        # Update layout settings
    fig.update_layout(showlegend=True,
            xaxis_title="Base Mean",
            yaxis_title="log2 Fold Change",
            width=figure_width,
            height=figure_height,
            plot_bgcolor='white',
            legend_title_text="Category",
            title_font=dict(family="Arial",color='black',size=titlesize_font))
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',
                 ticks="outside",tickson="boundaries",ticklen=5,tickcolor="black",
                 tickfont=dict(family="Arial",color='black',size=xax_tick_font),
                 title_font=dict(family="Arial",color='black',size=xax_font))

    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',
                 ticks="outside",tickson="boundaries",ticklen=5,tickcolor="black",
                 tickfont=dict(family="Arial",color='black',size=xax_tick_font),
                 title_font=dict(family="Arial",color='black',size=yax_font))


        # Show the plot
    fig.write_image('MAplot.png')
    st.plotly_chart(fig)
    
    save=st.download_button('PNG file name to save', data=open('MAplot.png','rb').read(), file_name='MAplot.png')
