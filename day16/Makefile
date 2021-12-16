all: day16

%: %.rs
	rustc $<

solve: day16
	./day16 input

test: day16
	@for test in test-*; do \
		echo ./day16 $$test; \
		./day16 $$test; \
		echo; \
	done

clean:
	rm -f day16
