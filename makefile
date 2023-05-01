target build_and_test:
	cmake -B _build -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/.local
	cmake --build _build
	_build/app/dftd4 dat.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 0.0 --pair-resolved
	# echo C_n.json start
	# cat C_n.json
	# echo C_n.json end
	# echo pairs.json start
	# cat pairs.json
	# echo pairs.json end
	echo .EDISP
	cp _build/app/dftd4 ~/.local/bin

test_edisp:
	_build/app/dftd4 dat.xyz


test_props:
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0
	# cp _build/app/dftd4 ~/.local/bin

test_2b:
	cmake -B _build -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/.local
	cmake --build _build
	_build/app/dftd4 dat.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 0.0
	mv .EDISP dimer.energy
	_build/app/dftd4 ma.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 0.0
	mv .EDISP ma.energy
	_build/app/dftd4 mb.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 0.0
	mv .EDISP mb.energy
	cp _build/app/dftd4 ~/.local/bin

test_ATM:
	cmake -B _build -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/.local
	cmake --build _build
	_build/app/dftd4 dat.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605
	mv .EDISP dimer.energy
	_build/app/dftd4 ma.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605
	mv .EDISP ma.energy
	_build/app/dftd4 mb.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605
	mv .EDISP mb.energy
	cp _build/app/dftd4 ~/.local/bin
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0
	test -f C_n.json && echo "C_n.json exists" && echo "copying dftd4 to ~/.local/bin" && cp _build/app/dftd4 ~/.local/bin

target test_props:
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0

.DEFAULT_GOAL := build_and_test
