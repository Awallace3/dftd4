target build_and_test:
	cmake -B _build -G Ninja -DCMAKE_INSTALL_PREFIX=$HOME/.local
	cmake --build _build
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0
	test -f C_n.json && echo "C_n.json exists" && echo "copying dftd4 to ~/.local/bin" && cp _build/app/dftd4 ~/.local/bin

target test_props:
	_build/app/dftd4 dat.xyz --property --param 1.0 0.9 0.4 5.0

.DEFAULT_GOAL := build_and_test
