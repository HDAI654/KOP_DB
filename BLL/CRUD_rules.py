from DAL.repository import CRUD
class rCRUD:
    def delete(self, address, tbl, value):
        c = CRUD()
        c.delete(address=address, tbl=tbl, value=value)
    def update(self, address, tbl, nv, ov):
        c = CRUD()
        c.update(address=address, tbl=tbl, nv=nv, ov=ov)
    def add(self, address, tbl, values):
        c = CRUD()
        c.add(address=address, tbl=tbl, values=values)