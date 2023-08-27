@echo off

echo Activating the virtual environment...
call Scripts\activate

echo Installing pip in the virtual environment...
python -m ensurepip --default-pip

echo Installing Python dependencies...
pip install -r requirements.txt
@echo off
set /p dbname=Enter the name of the database: 



set /p mysql_password=Enter MySQL password:

echo.
echo Creating MySQL database...
mysql -u root -p%mysql_password% --default-character-set=utf8mb4 -e "CREATE DATABASE IF NOT EXISTS %dbname%;"

echo.
echo Restoring MySQL database...
mysql -u root -p%mysql_password% --default-character-set=utf8mb4 %dbname% < dumptest.sql

echo.
echo Process completed.
pause
