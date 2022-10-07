target build_and_test:
	cmake -B _build -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/.local
	cmake --build _build
	_build/app/dftd4 dat.xyz --property --param 1.0 1.61679827, 0.44959224, 3.35743605 --mbdscale 0.0 --pair-resolved
	echo c6.txt start
	cat c6.txt
	echo c6.txt end
	echo c8.txt start
	cat c8.txt
	echo c8.txt end
	echo pairs.txt start
	cat pairs.txt
	echo pairs.txt end
	cp _build/app/dftd4 ~/.local/bin


test_props:
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0

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
