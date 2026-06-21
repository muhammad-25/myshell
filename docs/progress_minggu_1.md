# Progress Minggu Pertama

## Ringkasan

Pada minggu pertama, proyek custom shell difokuskan pada fondasi utama:
REPL loop, prompt, pembacaan input, tokenisasi command line, built-in `exit`,
dan error handling dasar. Implementasi dibuat modular supaya pengembangan
minggu berikutnya bisa dilanjutkan tanpa memindahkan banyak kode.

## Fitur Selesai

| Target | Status | Modul |
| --- | --- | --- |
| Prompt `myshell>` | Selesai | `prompt.py` |
| REPL loop | Selesai | `shell.py` |
| Input kosong tidak crash | Selesai | `shell.py` |
| Built-in `exit` | Selesai | `builtins/core.py` |
| Tokenisasi input | Selesai | `parser.py` |
| Error kutip tidak tertutup | Selesai | `parser.py`, `shell.py` |
| Riwayat input dasar | Selesai | `history.py` |

## Contoh Output

```text
myshell> ls -la
Token: ['ls', '-la']
myshell> echo "halo dunia"
Token: ['echo', 'halo dunia']
myshell> 
myshell> exit
Sampai jumpa!
```

## Alasan Struktur

Walaupun fitur minggu pertama masih sederhana, kode sudah dibagi menjadi
beberapa bagian seperti shell pada umumnya:

- `parser.py` bertanggung jawab memecah input menjadi token.
- `builtins/` menyimpan command internal seperti `exit`, `help`, dan `history`.
- `executor.py` menjadi tempat eksekusi command.
- `shell.py` mengatur REPL loop dan alur utama.
- `context.py` menyimpan status runtime seperti `running`, `last_status`, dan
  riwayat input.

## Rencana Lanjut

Minggu kedua dapat menambahkan built-in `cd` dan `pwd`, lalu executor untuk
perintah eksternal memakai `subprocess`. Minggu ketiga dapat melanjutkan ke
piping dan redirection.
