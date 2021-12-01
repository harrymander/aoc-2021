CFLAGS = -Wall -Werror

all: day1-1 day1-2

test: test.txt day1-1 day1-2
	./day1-1 $<
	./day1-2 $<

solve: input.txt day1-1 day1-2
	./day1-1 $<
	./day1-2 $<

clean:
	rm -f day1-1 day1-2
