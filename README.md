# pidMatDraw
Python scripts to calculate pairwise similarity (% identity) from multiple alignment and draw matrix as heatmap image

Contents

 pidMatDraw.py:  main script to calculate pairwise identity and draw matrix as triangle heatmap image
 doubleplotmatrix.py:  a script to draw two comparison matrix into half-half rectangle heatmap


Usage

    python pidMatDraw.py [tab-formatted alinged sequences] (options)


Dependent packages

  numpy, matplotlib, pandas, seaborn


Imput file

  tab-formatted aligned sequences


Recommendation for preparation of input file

  use sequence aligner (eg. MAFFT) and fasta-handling tool
  
  example of input file preparation
  
    mafft multifasta.fasta > multifasta_aligned.fasta
    
    seqkit fx2tab multifasta_aligned.fasta > multifasta_aligned.tab


options

    -o (--out) [output_prefix] : specify output prefix (dafault:none)
  
    -v (--withvalue) : print values into heatmap (default:no)
  
    -s (--square) : make heatmap cells square

