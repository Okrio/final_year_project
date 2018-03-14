#
# Makefile for Linux
#
C =		gcc -m32 -c -DUNIX -DLINUX
L =		gcc -m32
LIBS =		-ldl

all:  		ismain

ismain:		main.o isense.o
		$(L) -o $@ main.o isense.o $(LIBS)

main.o:		main.c *.h
		$(C) main.c

isense.o:	isense.c *.h
		$(C) isense.c

clean:
	  rm -f *.o ismain
