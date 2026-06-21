# MyShell Kelompok 9

Proyek ini adalah hasil progress minggu pertama custom shell menggunakan
Python. Kode tidak dibuat sebagai satu file tunggal, tetapi dipisah menjadi
beberapa modul agar bentuknya mendekati proyek shell yang umum: ada parser,
runtime context, built-in command, executor, prompt, dan launcher CLI.

## Target Minggu Pertama

- Menampilkan prompt `myshell>`.
- Membaca input user secara berulang dengan REPL loop.
- Keluar saat user mengetik `exit`.
- Mengabaikan input kosong tanpa crash.
- Memecah input menjadi token menggunakan `shlex`.
- Menangani tanda kutip yang tidak ditutup dengan pesan error.

## Struktur Proyek

```text
myshell/
|-- run.py
|-- pyproject.toml
|-- src/
|   `-- myshell/
|       |-- cli.py
|       |-- shell.py
|       |-- parser.py
|       |-- executor.py
|       |-- context.py
|       |-- prompt.py
|       |-- history.py
|       |-- errors.py
|       `-- builtins/
|           |-- base.py
|           |-- core.py
|           `-- __init__.py
|-- tests/
|-- docs/
`-- examples/
```

## Cara Menjalankan

```bash
python run.py
```

Contoh:

```text
myshell> ls -la
Token: ['ls', '-la']
myshell> cp file1.txt file2.txt
Token: ['cp', 'file1.txt', 'file2.txt']
myshell> exit
Sampai jumpa!
```

Untuk menjalankan satu perintah tanpa masuk mode interaktif:

```bash
python run.py -c "ls -la"
```

## Pengujian

```bash
python -m unittest discover -s tests
```

Catatan: pada minggu pertama, perintah eksternal belum benar-benar
dieksekusi. Perintah selain built-in akan ditampilkan sebagai token sebagai
bukti bahwa tahap tokenisasi sudah berjalan.
