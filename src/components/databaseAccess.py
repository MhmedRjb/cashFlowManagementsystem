import pandas as pd
from sqlalchemy import create_engine

class databaseAccess:
    def __init__(self, mysql=None,username=None, password=None, hostname=None, database=None):
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()
        self.engine = create_engine(f'mysql+pymysql://{username}:{password}@{hostname}/{database}')


    def _execute_sql(self, sql, params=None):
        self.cursor.execute(sql, params)
        self.conn.commit()

    def readsql(self, sql, params=None):
        self.cursor.execute(sql, params)
        data = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        data_df = pd.DataFrame(data, columns=columns)
        return data_df
    
    def call_sql(self, procedure_name, params=None):
        sql = f"{procedure_name}"
        self._execute_sql(sql, params)

    def export_data_first(self, data, table_name):
        #this function is used sqlalchemy unlike the other function 
        data.to_sql(table_name, self.engine, if_exists='replace', index=False)


    def update_data_in(self, table_name, set_values, column_name, values):
        set_clause = ', '.join([f"{col} = %s" for col in set_values.keys()])
        values_str = ', '.join(['%s' for _ in values])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {column_name} IN ({values_str})"
        self._execute_sql(sql, (*set_values.values(), *values))
    

    



    # ...

if __name__ == "__main__":
    # Values with my MySQL connection details
# Assume the class DatabaseHandler with the update_data_in method
    class DatabaseHandler:
        def update_data_in(self, table_name, set_values, column_name, values):
            set_clause = ', '.join([f"{col} = %s" for col in set_values.keys()])
            print("set_values.values()",set_values.keys())
            print('set_clause',set_clause)
            values_str = ', '.join(['%s' for _ in values])
            print('values_str',values_str)
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {column_name} IN ({values_str})"
            print('s')
            self._execute_sql(sql, (*set_values.values(), *values))
            result = self._execute_sql(sql, (*set_values.values(), *values))
            print('result',result)

        def _execute_sql(self, sql, params):
            # Assume this method handles the database connection and execution of the query
            # For simplicity, let's just print the SQL query and the parameters for illustration purposes.
            print("Executing SQL query:", sql)
            print("Query parameters:", params)
    

    # Create an instance of the DatabaseHandler class
    db_handler = DatabaseHandler()

    # Example values for the function parameters
    table_name = "employees"
    set_values = {"salary": 50000, "status": "active","salady": 5000}
    column_name = "employee_id"
    values = [101, 102, 103]

    # Call the update_data_in method with the example values
    db_handler.update_data_in(table_name, set_values, column_name, values)
