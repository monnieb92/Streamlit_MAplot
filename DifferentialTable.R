library(dplyr)
library(tidyverse)

result_table <- upload_file_df
result_table[is.na(result_table)] <- 1

result_table_filtered <- result_table %>% 
  mutate(FoldChange = ((2^(abs(log2FoldChange)))*sign(log2FoldChange))) %>% 
  transform( category = ifelse((padj <= adjp &  FoldChange <= -foldchangedn), "Down", ifelse((padj <= adjp &  FoldChange >= foldchangeup), "Up",  "NS")))

count_result <- dplyr::count(result_table_filtered, category)
