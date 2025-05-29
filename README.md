# sqlite_standalone
A standalone sqlite for external uses.

Build with Python and fastAPI.

# Dev/Build

`rundev.bat` to start dev server.

`runbuild.bat` to build. Find the built exe in the dist folder.

`runstart.bat` to try deployment environment.

# cmd options

`-port`: to start at given port, default 8000.

```
sqlte-standalone.exe -port 8025
```

# api

http://127.0.0.1:8000/docs#/

Replace 8000 with your port if you change it.

Normally you post to /sqlite/connect_in_memory to start the sqlite.

Then post { query string, parameters } to /sqlite/query to query. The format follows sqlite's parameterized query. Just becareful that query string accepts single quotes (sql standard), while parameters array accepts double quotes (json standard).



