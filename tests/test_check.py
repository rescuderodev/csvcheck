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
    return check(io.StringIO(text), schema)


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
