# csvcheck

Small command line tool to check a CSV file against a schema written in TOML:
required columns, types, allowed values, regex and unique columns.

I made it because I was tired of finding the broken row of an excel export by
hand. No dependencies (only the standard library), needs Python 3.11+ for
`tomllib`.

## Usage

```bash
pip install -e .
csvcheck examples/productos.csv --schema examples/schema.toml
```

```
row 5, precio: empty
row 6, id: duplicated, first seen in row 4
row 6, categoria: 'papeleria' not in ['libros', 'musica', 'cine']
5 rows, 3 problems
```

Exit code is 1 if there is any problem, so it can be used in scripts (`-q` for no output).

## Schema

```toml
[columns.id]
type = "int"        # str (default), int, float, date (YYYY-MM-DD)
unique = true

[columns.categoria]
allowed = ["libros", "musica", "cine"]

[columns.cp]
regex = "[0-9]{5}"
required = false    # columns are required by default
```

The delimiter is detected (`,` `;` or tab) and decimal comma is accepted, because
excel in spanish saves the files like that.

## Tests

```bash
pip install -e ".[test]"
pytest
```
