fmt:
	isort . && black -l 120 . 

check:
	mypy .
