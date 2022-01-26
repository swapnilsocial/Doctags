import os
import docx

doc = docx.getdocumenttext('/home/swap/swapnilsocial/Doctags/data/sampledata/file-sample_100kB.docx')
all_paras = doc.paragraphs
len(all_paras)