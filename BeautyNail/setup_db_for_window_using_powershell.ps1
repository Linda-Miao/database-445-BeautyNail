$ErrorActionPreference = "Stop"

# --- CONFIG ---
$DB_NAME="beautynailnet"
$DB_HOST="127.0.0.1"
$DB_PORT="3306"
$DB_USER="root"
$DB_PASS="root"   # <-- change

# Path to mysql.exe (edit if needed)
$MySql = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

# .sql files
$SQL1="sql\PhaseIII_Team 7_SQL script Submission"
$SQL2="sql\PhaseIII_Team 7_Script run after running migrations.sql"

function Invoke-MySqlFile {
    param([string]$FilePath, [string]$DbName = "")
    if (-not (Test-Path $FilePath)) { throw "SQL file not found: $FilePath" }
    $posix = $FilePath -replace '\\','/'                # safer for mysql on Windows
    $src   = "SOURCE `"$posix`";"                       # quote inside -e
    $args  = @(
        "--no-defaults",
        "-h", $DB_HOST,
        "-P", $DB_PORT,
        "-u$DB_USER",          # NOTE: no space
        "-p$DB_PASS"           # NOTE: no space
    )
    if ($DbName) { $args += $DbName }
    $args += @("-e", $src)
    & $MySql @args
}

# 0) Sanity: can we talk to MySQL?
& $MySql --no-defaults -h $DB_HOST -P $DB_PORT -u$DB_USER -p$DB_PASS -e "SELECT 1;"

# 1) Ensure DB exists (safe if already created by SQL1)
& $MySql --no-defaults -h $DB_HOST -P $DB_PORT -u$DB_USER -p$DB_PASS `
  -e "CREATE DATABASE IF NOT EXISTS `$DB_NAME` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"

# 2) Run SQL 1 (schema/seed)
Invoke-MySqlFile -FilePath $SQL1

# 3) Django migrate
python manage.py migrate

# 4) Run SQL 2 (depends on Django tables)
Invoke-MySqlFile -FilePath $SQL2 -DbName $DB_NAME

Write-Host "Database setup complete."
