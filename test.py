#!/usr/bin/python
"""Alter all tables with fks constraints and add on delete cascade
"""
import psycopg2
from subprocess import call
import psycopg2.extras


def make_drop_add_cascade(tblbase, fkname, tblreferenced, pkname):
    query = ""
    query += "ALTER TABLE "
    query += tblbase
    query += " DROP CONSTRAINT "
    query += fkname
    query += ", ADD CONSTRAINT "
    query += fkname
    query += " FOREIGN KEY ("
    query += pkname
    query += ") "
    query += " REFERENCES "
    query += tblreferenced
    query += "("
    query += pkname
    query += ") "
    query += "ON DELETE CASCADE;"
    return query

def make_alter_table(r):
  t_base = r[0] #Tabla que posee la FK
  fk_name = r[1]
  pk_name = r[2]
  t_ref = r[3] #Tabla a la que se hace referencia
  new_query = make_drop_add_cascade(t_base, fk_name, t_ref, pk_name)
  print fk_name
  return new_query

def main():
    query = """SELECT
                distinct(tc.table_name),
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.referential_constraints as rc
                  ON rc.constraint_name = tc.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
            WHERE constraint_type = 'FOREIGN KEY' AND
                tc.constraint_schema = 'public' AND
                tc.constraint_name like '%idioma%' AND
                tc.table_name != 'tbl_idiomas' AND
                kcu.column_name != 'idioma_id' AND
                rc.delete_rule = 'NO ACTION'"""

    try:
        conn = psycopg2.connect("dbname='suit' user='postgres' host='192.168.0.8' password='123456'")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        #print rows
        with open("log-sql-v1.73.sql", 'w') as out:
            for row in rows:
                line = make_alter_table(row)
                out.write(line)
                out.write("\n")
            #print row['constraint_name']
        call(["atom", "log-sql-v1.73.sql"])

    except:
        print "I am unable to connect to the database"

if __name__ == '__main__':
    main()
