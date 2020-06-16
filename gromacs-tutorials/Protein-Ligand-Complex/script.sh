grep JZ4 3HTB_clean.pdb > jz4.pdb
gmx pdb2gmx -f 3HTB_clean_no_legand.pdb  -o 3HTB_processed.gro
cp 3HTB_processed.gro complex.gro
/Users/jayanti/anaconda3/envs/mol_dnm/bin/python scripts/cgenff_charmm2gmx_py3_nx1.py     JZ4 jz4_fix.mol2 jz4_fix.str  charmm36-jul2017.ff
gmx editconf -f jz4_ini.pdb -o jz4.gro
