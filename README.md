# Streamlit_MAplot
## This is a streamlit app to determine differential analysis of DESeq2 datasets and create a MA plot of the data. 
![Uploading and naming your file](./Images_github_maplot/DragDrop_Titles.png)
1. Upload the .txt file from DESeq2 output.
2. Create a unique name for the files
3. Select the adjusted p-value you want: 0.05 is what is typically recommended
4. Select the FoldChange you want to use when selecting the differentially changed genes or chromosomal locations.
![Figure Formating](./Images_github_maplot/colnam_title.png)
5. Make sure the column names in your .txt file match what is in the log2FoldChange and padj, or change the column names in the app.
![Figure Formating](./Images_github_maplot/FigureFormat.png)
6. Select the column name you want to visualize on the .HTML plot, typically it would be gene_name or transcript id
7. Adjust any of the figure formating for your MA plot such as font size, number of ticks, image size, etc.
![Figure Formating](./Images_github_maplot/TickRange.png)
8. For the number of ticks on the y-axis (baseMean) here is the typical outcome for each number:
   *1 = 10^1^
   *2 = 10^2^
   *3 = 10^3^
   *4 = 10^4^
   *5 = 10^5^
   *6 = 10^6^
9. Run analysis and have fun!
https://differentialanalysismaplot.streamlit.app/
