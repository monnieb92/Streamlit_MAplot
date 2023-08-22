library(dplyr)
library(tidyverse)

# Read command-line arguments
args <- commandArgs(trailingOnly = TRUE)
df <- args[4] 

result_table <- read.csv(df, sep = " ")

result_table[is.na(result_table)] <- 1

result_table_filtered <- result_table %>% 
  mutate(FoldChange = ((2^(abs(log2FoldChange)))*sign(log2FoldChange))) %>% 
  transform( category = ifelse((padj <= adjp &  FoldChange <= -foldchangedn), "Down", ifelse((padj <= adjp &  FoldChange >= foldchangeup), "Up",  "NS")))

counts_table <- dplyr::count(result_table_filtered, category)
counts_table
