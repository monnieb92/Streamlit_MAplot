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
   * 1 = 10<sup>1</sup>
   * 2 = 10<sup>2</sup>
   * 3 = 10<sup>3</sup>
   * 4 = 10<sup>4</sup>
   * 5 = 10<sup>5</sup>
   * 6 = 10<sup>6</sup>
9. Run analysis and have fun! <br>
https://differentialanalysismaplot.streamlit.app/

###Example of a MA plot:<br>

<img src="./Images_github_maplot/MAplot-9.png" width="300" height="300">
