# vulnerable_app.py
import subprocess
import pickle
import sqlite3
import sys
API_KEY=sk_test_FAKE1234567890abcdefghijklmnopqrstuv
# 1) insecure eval (RCE risk)
def compute(expr):
    # WARNING: unsafe use of eval
    return eval(expr)

# 2) insecure subprocess with shell=True using user input
def list_files(path):
    # WARNING: shell injection possible if path contains malicious content
    return subprocess.check_output(f"dir {path}", shell=True, text=True)

# 3) insecure deserialization (pickle.loads on untrusted data)
def load_object(serialized_bytes):
    # WARNING: insecure deserialization
    return pickle.loads(serialized_bytes)

# 4) SQL injection via string formatting
def find_user(conn, username):
    cur = conn.cursor()
    sql = f"SELECT id, username FROM users WHERE username = '{username}'"
    cur.execute(sql)
    return cur.fetchall()

# 5) weak crypto example placeholder (not implemented) - CodeQL might flag other patterns
# Minimal demonstration of a "main" that triggers flows
def main():
    print("Vulnerable demo app")
    # eval usage (SAST should flag)
    try:
        print("eval result:", compute("2+2"))
    except Exception as e:
        print("eval error:", e)

    # subprocess usage (SAST should flag)
    try:
        print("Listing current dir:")
        print(list_files("."))
    except Exception as e:
        print("subprocess error:", e)

    # sqlite demo for SQL injection
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
    conn.execute("INSERT INTO users (username) VALUES ('alice')")
    conn.commit()
    print("Querying user alice (safe):", find_user(conn, "alice"))

    # insecure pickle demo: DO NOT RUN with untrusted data
    s = pickle.dumps({"ok": True})
    print("Deserialized (safe local):", load_object(s))

if __name__ == "__main__":
    main()
