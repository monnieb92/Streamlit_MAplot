library(dplyr)
library(tidyverse)

# Read command-line arguments
args <- commandArgs(trailingOnly = TRUE)
adjp <- as.numeric(args[1])
foldchangeup <- as.numeric(args[2])
foldchangedn <- as.numeric(args[3])
input_file <- args[4]

result_table <- read.csv(input_file, sep = " ")

result_table[is.na(result_table)] <- 1

result_table_filtered <- result_table %>% 
  mutate(FoldChange = ((2^(abs(log2FoldChange)))*sign(log2FoldChange))) %>% 
  transform( category = ifelse((padj <= adjp &  FoldChange <= -foldchangedn), "Down", ifelse((padj <= adjp &  FoldChange >= foldchangeup), "Up",  "NS")))

counts_table <- dplyr::count(result_table_filtered, category)
counts_table
