.PHONY: clean

# релизный запуск парсинга ссылок
run: main.c links.txt
	gcc -pthread main.c -o app.exe -DDEBUG=0
	./app.exe

gcov: main.c links.txt
	gcc -pthread -fprofile-arcs -ftest-coverage -o app.exe -DDEBUG=0 main.c
	./app.exe
#	gcov app-main.c

# дебажная сборка приложения
debug: main.c links.txt
	gcc -pthread main.c -o app.exe -DDEBUG=1

# дебажный запуск парсинга ссылок
debug-run: main.c links.txt
	gcc -pthread main.c -o app.exe -DDEBUG=1
	./app.exe

# генерация ссылок
generate_links: generate_links.py
	python3 generate_links.py

# преобразование замеров из текстового файла в график и сохранение
draw_graph: measure.txt
	python3 graph.py

clean:
	rm -f *.exe *.out