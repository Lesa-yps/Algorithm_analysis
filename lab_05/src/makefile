.PHONY: clean

CC = gcc
CFLAGS = -pthread 
SQLFLAGS =  -I/usr/include/postgresql
LDFLAGS = -L/usr/lib -lpq
GCOVFLAGS = -fprofile-arcs -ftest-coverage

# релизный запуск приложения
run: main.c create.sql lib_list.o work_db.o
	$(CC) $(CFLAGS) -DDEBUG=0 $(SQLFLAGS) main.c -o app.exe $(LDFLAGS) lib_list.o work_db.o
	./app.exe

%.o: %.c
	$(CC) $(SQLFLAGS) $< -o $@ -c

gcov: main.c create.sql lib_list.o work_db.o
	$(CC) $(CFLAGS) $(GCOVFLAGS) -DDEBUG=0 $(SQLFLAGS) main.c -o app.exe $(LDFLAGS) lib_list.o work_db.o
	./app.exe
	gcov app-main.c

# релизная сборка приложения
release: main.c create.sql lib_list.o work_db.o
	$(CC) $(CFLAGS) -DDEBUG=0 $(SQLFLAGS) main.c -o app.exe $(LDFLAGS) lib_list.o work_db.o

# дебажная сборка приложения
debug: main.c create.sql lib_list.o work_db.o
	$(CC) $(CFLAGS) $(GCOVFLAGS) -DDEBUG=0 $(SQLFLAGS) main.c -o app.exe $(LDFLAGS) lib_list.o work_db.o

# преобразование замеров из текстового файла в график и сохранение
draw_graph: measure.txt
	python3 graph.py

clean:
	rm -f *.exe *.out *.o