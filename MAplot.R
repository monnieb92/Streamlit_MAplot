library(ggplot2)
library(tidyverse)
library(dplyr)

result_table <- read_csv(uploaded_file)
result_table[is.na(result_table)] <- 1

result_table_filtered <- result_table %>% 
  dplyr::mutate(FoldChange = ((2^(abs(log2FoldChange)))*sign(log2FoldChange))) %>% 
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
