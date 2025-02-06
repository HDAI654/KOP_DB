import sqlite3
class CRUD:
    def get_fields(self, address, tbl):
        try:
            conn = sqlite3.connect(str(address))
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {tbl}")
            conn.commit()
            conn.close()
            names = [description[0] for description in cursor.description]
            return names
        except:
            pass
    def delete(self, address, tbl, value):
        try:
            fields = self.get_fields(address=address, tbl=tbl)
            conn = sqlite3.connect(str(address))
            cursor = conn.cursor()
            cursor.execute(f"delete from {tbl} where {fields[0]}='{value[0]}'")
            conn.commit()
            conn.close()
        except:
            pass
    def update(self, address, tbl, nv, ov):
        try:
            fields = self.get_fields(address=address, tbl=tbl)
            bq = ["update ", str(tbl), " set "]
            
            # make tuples (field, new value) and (field, old value)
            old_value = []
            new_value = []
            for o in ov:
                old_value.append((fields[ov.index(o)], o))
            for n in nv:
                new_value.append((fields[nv.index(n)], n))

            # add new value query to bq
            for nf, nv in new_value:
                if (nf, nv)==new_value[-1]:
                    poq = f"{nf}='{nv}'"
                else:
                    poq = f"{nf}='{nv}', "
                bq.append(poq)
            bq.append(" where ")

            # add old value query to bq
            for of, ov in old_value:
                if (of, ov)==old_value[-1]:
                    opoq = f"{of}='{ov}'"
                else:
                    opoq = f"{of}='{ov}' and "
                bq.append(opoq)
            bq.append(" ;")
            mq = "".join(bq)
            # run query
            conn = sqlite3.connect(str(address))
            cursor = conn.cursor()
            cursor.execute(str(mq))
            conn.commit()
            conn.close()
        except:
            pass
    def add(self, address, tbl, values):
        try:
            conn = sqlite3.connect(str(address))
            cursor = conn.cursor()
            cursor.execute(f"insert into {tbl} values {tuple(values)};")
            conn.commit()
            conn.close()
        except:
            pass