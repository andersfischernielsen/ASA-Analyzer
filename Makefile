.PHONY: all clean
TARGETS=analyzer.native analyzer.byte _build/example.cma _build/example.cmxs
all: $(TARGETS)
clean:
	rm -f $(TARGETS)
	rm -rf _build

analyzer.native: _build/analyzer.native
analyzer.byte: _build/analyzer.byte

_build/%: *.ml*
	ocamlbuild -use-ocamlfind $*
