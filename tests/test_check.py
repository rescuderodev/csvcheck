import io

from csvcheck import check

SCHEMA = {
    "columns": {
        "id": {"type": "int"},
        "nombre": {"type": "str"},
        "precio": {"type": "float"},
        "fecha_alta": {"type": "date", "required": False},
    }
}


def run(text, schema=SCHEMA):
    problems, _ = check(io.StringIO(text), schema)
    return problems


def test_ok():
    assert run("id,nombre,precio,fecha_alta\n1,uno,9.5,2026-08-01\n") == []


def test_missing_column():
    problems = run("id,nombre\n1,uno\n")
    assert [p.column for p in problems] == ["precio"]


def test_bad_types():
    problems = run("id,nombre,precio,fecha_alta\nx,uno,caro,01/08/2026\n")
    assert {p.column for p in problems} == {"id", "precio", "fecha_alta"}


def test_empty_required():
    problems = run("id,nombre,precio,fecha_alta\n1,,3,\n")
    assert [(p.row, p.column) for p in problems] == [(2, "nombre")]


def test_allowed_and_regex():
    schema = {"columns": {"cat": {"allowed": ["libros", "musica"]}, "cp": {"regex": "[0-9]{5}"}}}
    problems = run("cat,cp\nlibros,28002\ncine,2800\n", schema)
    assert [(p.row, p.column) for p in problems] == [(3, "cat"), (3, "cp")]


def test_semicolon_and_decimal_comma():
    assert run("id;nombre;precio;fecha_alta\n1;uno;9,5;2026-08-01\n") == []


def test_unique():
    schema = {"columns": {"id": {"type": "int", "unique": True}}}
    problems = run("id\n1\n2\n1\n", schema)
    assert len(problems) == 1 and "row 2" in problems[0].message


def test_row_count():
    _, rows = check(io.StringIO("id,nombre,precio\n1,a,1\n2,b,2\n"), SCHEMA)
    assert rows == 2
