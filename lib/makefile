all: CLIB

OBJ := $(patsubst %.c,%.o,$(wildcard *.c))

%.o: %.c
	$(CC) -c -g -o $*.o $<

CLIB: $(OBJ)
	$(CC) -fPIC -shared -o clib.so $+ -L. -lm

clean:
	rm ./*.o
