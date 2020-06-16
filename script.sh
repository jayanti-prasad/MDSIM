# Set some environment variables 
FREE_ENERGY=`pwd`
MDP=$FREE_ENERGY

GMX=/usr/local/gromacs/bin/

LAMBDA=0
   
$GMX/gmx grompp -f $MDP/em_steep_$LAMBDA.mdp -c $FREE_ENERGY/methane_water.gro -p $FREE_ENERGY/topol.top -o min$LAMBDA.tpr
$GMX/gmx mdrun -deffnm min$LAMBDA -nt 4

