#!/bin/python 

import streamlit as st
import subprocess
from PIL import Image

st.header('Differential Analysis of DESEQ2 Data')

st.sidebar.markdown('''
# About
This demo shows the use of R in a Streamlit App by showcasing 3 example use cases.

The R code for all 3 examples are rendered on-the-fly in this app.

R packages used:
- `dplyr`
- `ggplot2`
- `tidyverse`
- `readr`
''')

uploaded_file = st.sidebar.file_uploader("Upload your input txt file", type=["txt"])
st.write('This is the path to the csv file from DESEQ2', uploaded_file)

adjp = st.number_input('adjusted p-value')
st.write('The current adjusted p-value is ', adjp)

foldchangeup = st.number_input('Fold Change Up')
st.write('The current Fold Change for up regulated is ', foldchangeup)

foldchangedn = st.number_input('Fold Change Down')
st.write('The current Fold Change for down regulated is ', foldchangedn)

st.subheader('1. Determining Differential analysis using')
with st.expander('See code'):
  code1 = '''
library(ggplot2)
library(dplyr)
library(tidyverse)
library(readr)
  
result_table <- read_tsv(uploaded_file)
result_table[is.na(result_table)] <- 1

result_table_filtered <- result_table %>% 
  mutate(FoldChange = ((2^(abs(log2FoldChange)))*sign(log2FoldChange))) %>% 
  transform( category = ifelse((padj <= adjp &  FoldChange <= -foldchangedn), "Down", ifelse((padj <= adjp &  FoldChange >= foldchangeup), "Up",  "NS")))

count_result <- dplyr::count(result_table_filtered, category)

theme_monica <- function(){
  theme_classic() %+replace%    #replace elements we want to change
    #font <- "Times", 
    theme(
      
      plot.title = element_text(             #title
        family = "sans",              #set font family
        size = 20,                #set font size
        face = 'bold',            #bold typeface
        hjust = 0.5,                #left align
        vjust = 2),               #raise slightly
      
      plot.subtitle = element_text(          #subtitle
        family = "sans",            #font family
        size = 14),               #font size
      
      plot.caption = element_text(           #caption
        family = "sans",            #font family
        size = 10,                 #font size
        hjust = 1),               #right align
      legend.text = element_text(             #axis titles
        family =  "sans",            #font family
        face = 'bold',
        size = 12),
      axis.title = element_text(             #axis titles
        family = "sans",            #font family
        face = 'bold',
        size = 16),               #font size
      
      axis.text = element_text(              #axis text
        family = "sans",            #axis famuly
        face = 'bold',
        size = 16),                #font size
      
      #axis.text.x = element_text(            #margin for axis text
      #margin=margin(10, b = 12))
      
    )}

MAplotoutput <- ggplot(result_table_filtered, aes(y = log2FoldChange, x = baseMean, color = category)) +
  geom_point( size = 0.35) + theme_monica() + 
  theme(panel.border = element_rect(fill=NA, colour = "black", size=1)) +
  scale_color_manual(breaks = c("Up", "NS", "Down"), values=c('#ca0020','#bababa','#0571b0')) +
  geom_hline(yintercept=0, linetype="solid", color = "black", size=1) +
  scale_y_continuous(breaks=seq(-4, 4, 1), limits=c(-4,4)) +
  #scale_x_continuous(breaks=seq(0, 650, 50), limits=c(0,655)) 
  scale_x_log10(breaks = c(10,100,1000,10000)) +
  expand_limits(x=c(0,10000))

print(MAplotoutput)

ggsave("MAplot.png", plot = MAplotoutput ,width = 4.25, height = 3, dpi = 300)

 '''

st.code(code1, language='R')
process2 = subprocess.Popen(["Rscript", "MAplot.R", str(uploaded_file),str(adjp), str(foldchangeup), str(foldchangedn)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result2 = process2.communicate()
st.write("Count Results:")
st.write(result2)

#image = Image.open('MAplot.png')
#st.image(image)

