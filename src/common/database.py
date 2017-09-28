import sqlite3

dbPath = "./src/data/test.db"
#dbPath = "../data/test.db"

def SQL(sql):
	conn = sqlite3.connect(dbPath, check_same_thread = False)
	value = []
	c = conn.cursor()
	cursor = c.execute(sql)
	if ("select" or "SELECT") not in sql:
		conn.commit()
		conn.close()
	else:
		for row in cursor:
			value.append(row)
	conn.close()
	return value	

if __name__ == "__main__":

	#SQL("INSERT INTO SCANASE (ID,PRODUCTNAME,IP) \
    #  VALUES (1, 'Beoplay M3', '10.10.10.111')")
	#SQL("INSERT INTO STATUS (ID,SCAN,STATUS) VALUES (1, 'ase_scan', 0)")
	#SQL("delete from status")
	SQL("update status set STATUS=0 where SCAN='ase_scan'")
	print(SQL("select * from scanase"))
	print(SQL("select * from status"))