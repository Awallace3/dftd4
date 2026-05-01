_build/app/dftd4 water_he.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 1.0 --pair-resolved --charge 0
cp ./C_n.json C_n_water_he.json
_build/app/dftd4 water_he_1000.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 1.0 --pair-resolved --charge 0
cp ./C_n.json C_n_water_he_1000.json
_build/app/dftd4 water.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 1.0 --pair-resolved --charge 0
cp ./C_n.json C_n_water.json
_build/app/dftd4 he.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 1.0 --pair-resolved --charge 0
cp ./C_n.json C_n_he.json
