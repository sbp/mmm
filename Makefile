.PHONY: all
all: druler pmproofs.json pmsubtrees.txt pmdiversity.txt

druler: drule.c druler.c.patch
	cp drule.c druler.c
	patch -p1 < druler.c.patch
	gcc -O3 -o druler druler.c

pmproofs.json: pmparser.py pmproofs.txt
	python3 pmparser.py pmproofs.txt > pmproofs.json

pmsubtrees.txt: pmsubtrees.py pmproofs.json
	python3 pmsubtrees.py pmproofs.json > pmsubtrees.txt

pmdiversity.txt: pmdiversity.py pmsubtrees.txt
	python3 pmdiversity.py pmsubtrees.txt > pmdiversity.txt

# The following are not included in all

# Warning: This make rule is very slow
proofs15.txt.gz: trees.py dtrie.py
	rm -f proofs15.txt.gz
	python3 trees.py 15 | python3 dtrie.py cw proofs15.txt.gz -

# Warning: This make rule is EXTREMELY slow
proofs17.txt: trees.py dtrie.py proofs15.txt.gz
	python3 trees.py 17 | \
		python3 dtrie.py rw proofs15.txt.gz - > proofs17.txt
	python3 pmsearch.py pmsubtrees.txt proofs17.txt | grep DISCOVERY

.PHONY: discovery
discovery: pmsearch.py pmsubtrees.txt proofs15.txt.gz
	python3 pmsearch.py pmsubtrees.txt proofs15.txt.gz | grep DISCOVERY

.PHONY: test
test: dproof.py dprooftests.py pmproofs.json
	python3 dprooftests.py
