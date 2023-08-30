#!/bin/python 

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import StringIO

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

# Button click to create MA plot
if st.button('Create MA plot'):
    if result_table_df.empty():
        st.write("Please perform the differential analysis first.")
    else:
        # Create the MA plot using Plotly
        fig = px.scatter(result_table_df,
            x='baseMean',
            y='log2FoldChange',
            color='category',
            color_discrete_map={'Up': '#ca0020', 'NS': '#bababa', 'Down': '#0571b0'},
            opacity=0.6,
            title="MA Plot"
        )

        # Add horizontal line at y = 0
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=min(result_table_filtered['baseMean']),
                x1=max(result_table_filtered['baseMean']),
                y0=0,
                y1=0,
                line=dict(color="black", width=1),
            )
        )

        # Set log scale for x-axis
        fig.update_xaxes(type="log")

        # Set y-axis limits and ticks
        fig.update_yaxes(ticks="outside", tickvals=list(range(-4, 5)), range=[-4, 4])

        # Set x-axis ticks for log scale
        fig.update_xaxes(ticks="outside", tickvals=[10, 100, 1000, 10000])

        # Update layout settings
        fig.update_layout(
            showlegend=True,
            xaxis_title="Base Mean",
            yaxis_title="log2 Fold Change",
            width=800,
            height=600,
            plot_bgcolor='white',
            legend_title_text="Category"
        )

        # Show the plot
        st.plotly_chart(fig)

        # If you want to save the plot as an image
    
        plt.savefig('MAplot.png')
        st.pyplot(fig)
        save=st.download_button('PNG file name to save', data=open('MAplot.png','rb').read(), file_name='MAplot.png',width=800, height=600, scale=2)
