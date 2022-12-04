# UrFU Python

Репо для выполнения заданий, связанных с курсом
"Технологии программирования на Python"
(2 курс, ИРИТ-РТФ).

## Установка зависимостей (Arch Linux)
```sh
pip install -r requirements.txt
paru -S wkhtmltopdf-static
```

## Задания

### Тесты

![tests](/docs/tests.png)

### Профилизатор

<details>
  <summary>Вывод тестирования функций на время</summary>
Исходя из результата, лучшей оказалась вторая функция.

    test1 2.3689908319993265
    test2 0.07577202500033309
    test3 0.31943320199934533
    test4 0.4372644129998662
    test1
            29 function calls in 0.000 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 <string>:1(<module>)
            1    0.000    0.000    0.000    0.000 _strptime.py:26(_getlang)
            1    0.000    0.000    0.000    0.000 _strptime.py:318(_strptime)
            1    0.000    0.000    0.000    0.000 _strptime.py:574(_strptime_datetime)
            1    0.000    0.000    0.000    0.000 locale.py:384(normalize)
            1    0.000    0.000    0.000    0.000 locale.py:467(_parse_localename)
            1    0.000    0.000    0.000    0.000 locale.py:575(getlocale)
            1    0.000    0.000    0.000    0.000 profiling.py:9(test1)
            1    0.000    0.000    0.000    0.000 {built-in method _locale.setlocale}
            1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
            2    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
            3    0.000    0.000    0.000    0.000 {built-in method builtins.len}
            1    0.000    0.000    0.000    0.000 {built-in method strptime}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
            1    0.000    0.000    0.000    0.000 {method 'end' of 're.Match' objects}
            3    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
            1    0.000    0.000    0.000    0.000 {method 'groupdict' of 're.Match' objects}
            1    0.000    0.000    0.000    0.000 {method 'keys' of 'dict' objects}
            1    0.000    0.000    0.000    0.000 {method 'lower' of 'str' objects}
            1    0.000    0.000    0.000    0.000 {method 'match' of 're.Pattern' objects}
            1    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
            2    0.000    0.000    0.000    0.000 {method 'toordinal' of 'datetime.date' objects}
            1    0.000    0.000    0.000    0.000 {method 'weekday' of 'datetime.date' objects}


    test2
            6 function calls in 0.000 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 <string>:1(<module>)
            1    0.000    0.000    0.000    0.000 profiling.py:13(test2)
            1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
            1    0.000    0.000    0.000    0.000 {built-in method fromisoformat}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
            1    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}


    test3
            8 function calls in 0.000 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 <string>:1(<module>)
            1    0.000    0.000    0.000    0.000 profiling.py:17(test3)
            1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
            4    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}


    test4
            12 function calls in 0.000 seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.000    0.000    0.000    0.000 <string>:1(<module>)
            1    0.000    0.000    0.000    0.000 profiling.py:22(test4)
            1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
            1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
            8    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}


    test1 0:00:00.000065
    test2 0:00:00.000005
    test3 0:00:00.000009
    test4 0:00:00.000011
</details>

![profiler](/docs/profiler.png)
