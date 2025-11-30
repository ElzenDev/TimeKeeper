import sqlite3, os
from datetime import datetime, timezone
from typing import List, Dict, Any

class Database:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(os.path.dirname(script_dir), "data" ,"processes.db") 
        self.db_path: str = db_path
        self.initialize_database()
        
    def initialize_database(self):
        """
        Private method to set up the Tables
        """
        # connect to the database
        with sqlite3.connect(self.db_path) as conn:
            # Create a cursor that will be used to do pretty much everything in the database
            cursor = conn.cursor()

            cursor.executescript(
                """
                CREATE TABLE IF NOT EXISTS processes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    username TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name)
                );
                
                CREATE TABLE IF NOT EXISTS process_sessions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    process_session_id INTEGER REFERENCES processes(id),
                    pid INTEGER NOT NULL,
                    name TEXT,
                    category TEXT,
                    username TEXT,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP NULL,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_sessions_pid ON process_sessions(pid);
                CREATE INDEX IF NOT EXISTS idx_sessions_process ON process_sessions(process_session_id, start_time);
                """
            )
            
            conn.commit()


    def sync_processes(self, current_processes: List[Dict[str, Any]]) -> None:
        """ 
        Syncs current running processes with the database.
        This is Called once every monitoring cycle
        """
        now = datetime.now(timezone.utc)
        current_pids = {proc['pid'] for proc in current_processes}
        with sqlite3.connect(self.db_path) as  conn:
            
            # Handle Processes that are just registered (NEW PROCESSES)
            self.handle_new_process(conn, current_processes, now)
            
            # Updates the existing processes data (EXISTING PROCESSES)
            self.handle_existing_process(conn, current_processes, now)

            # Handle processes that stopped running (DISAPPEARD PROCESSES)
            self.handle_disappeard_process(conn, current_pids, now)

    
    def handle_new_process(self, conn: sqlite3.Connection, current_processes: List[Dict[str, Any]], now: datetime):
        """
        Handle newly added Processes.
        Creates a process entry and session
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for proc in current_processes:
                pid = proc['pid']
                name = proc['name']
                
                exists = cursor.execute(
                """
                -- If the end_time is Null it means that the process is still running, therefore it exists
                SELECT id FROM process_sessions
                WHERE pid = ? AND end_time IS NULL    
                """,(pid,)).fetchone()            
                
                if not exists:
                    
                    # New Process, so, create process entry
                    process_session_id = self.get_or_create_process(conn, proc, now)

                    # Create new session
                    cursor.execute("""
                        INSERT INTO process_sessions
                        (process_session_id, pid, name, category, username, start_time, last_seen)
                        VALUES(?, ?, ?, ?, ?, ?, ?)
                    """, (
                        process_session_id,
                        pid,
                        name,
                        proc['category'],
                        proc['username'],
                        now, # Start_time/ First_seen = now (when it is first detected)
                        now # Last Seen
                    ))
                    print("New Process Session Handled")
            conn.commit()
            

    def handle_existing_process(self, conn: sqlite3.Connection, current_processes: List[Dict[str, Any]], now: datetime):
        """
        Updates process info
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for proc in current_processes:
                pid = proc['pid']

                exists = cursor.execute(
                """
                -- If the end_time is Null it means that the process is still running, therefore it exits
                SELECT id FROM process_sessions
                WHERE pid = ? AND end_time IS NULL    
                """, (pid,)).fetchone() 

                if exists:
                    
                    cursor.execute(""" 
                        UPDATE process_sessions
                        SET
                            last_seen = ?
                        WHERE pid = ? AND end_time IS NULL
                    """,(now,pid))
            conn.commit()
       

    def handle_disappeard_process(self, conn: sqlite3.Connection, current_pids: set, now: datetime):
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get processes still running
            active_sessions = cursor.execute(
                """
                SELECT id, pid, last_seen FROM process_sessions
                WHERE end_time IS NULL;
                """
                ).fetchall()
            
            for session_id, pid, last_seen_str in active_sessions:
                if pid not in current_pids:
                    
                    last_seen = now.fromisoformat(last_seen_str)

                    cursor.execute("""
                        UPDATE process_sessions
                        SET end_time = ?
                        WHERE id = ?
                    """, (last_seen, session_id))
            conn.commit()


    def get_or_create_process(self, conn: sqlite3.Connection, proc: Dict, now: datetime) -> int:
        """Get existing process ID or create new process entry."""
        with conn as conn:
            cursor = conn.cursor()

            result = cursor.execute("""
                SELECT id FROM processes WHERE name = ?
            """, (proc['name'],)).fetchone()

            if result:
                # Update if process was already seen
                cursor.execute(
                    """
                    UPDATE processes SET last_seen = ? WHERE id = ?
                    """,
                    (now, result[0]))
                conn.commit()
                return result[0]
            else:
                
                # Create new procees entry
                cursor = cursor.execute(
                    """
                    INSERT INTO processes (name, username, first_seen, last_seen)
                    VALUES (?, ?, ?, ?)
                    """,(proc['name'], proc['username'], now, now)
                )
                
                conn.commit()
                return cursor.lastrowid
        

    def get_today_running_time(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            results = cursor.execute(
                """
                WITH process_windows AS (
                    -- First, identify distinct time windows for each process name
                    SELECT
                        p.name,
                        MIN(ps.start_time) as window_start,
                        CASE 
                            WHEN MAX(ps.end_time) IS NULL THEN 'now'
                            ELSE MAX(ps.end_time)
                        END as window_end
                    FROM processes p
                    JOIN process_sessions ps ON p.id = ps.process_session_id
                    WHERE date(ps.start_time, 'localtime') = date('now', 'localtime')
                    GROUP BY 
                        p.name,
                        -- Group by hourly windows to handle cases where the app was closed and reopened
                        strftime('%Y-%m-%d %H', ps.start_time)
                ),
                time_sums AS (
                    SELECT
                        name,
                        ROUND(
                            (julianday(window_end, 'localtime') - julianday(window_start)) * 86400 - 3600
                        ) as session_seconds
                    FROM process_windows
                )
                SELECT
                    name,
                    CAST(COALESCE(SUM(session_seconds), 0) AS INTEGER) as total_seconds
                FROM time_sums
                GROUP BY name
                ORDER BY total_seconds DESC
                """
            ).fetchall()
            return [{'name': row['name'], 'total_seconds': row['total_seconds']} for row in results]
   

    def get_week_running_time(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            results = cursor.execute(
                """
                WITH process_windows AS (
                    -- First, identify distinct time windows for each process name
                    SELECT
                        p.name,
                        MIN(ps.start_time) as window_start,
                        CASE 
                            WHEN MAX(ps.end_time) IS NULL THEN 'now'
                            ELSE MAX(ps.end_time)
                        END as window_end
                    FROM processes p
                    JOIN process_sessions ps ON p.id = ps.process_session_id
                    WHERE strftime('%Y-%W', ps.start_time, 'localtime') = strftime('%Y-%W', 'now', 'localtime')
                    GROUP BY 
                        p.name,
                        -- Group by hourly windows to handle cases where the app was closed and reopened
                        strftime('%Y-%m-%d %H', ps.start_time)
                ),
                time_sums AS (
                    SELECT
                        name,
                        ROUND(
                            (julianday(window_end, 'localtime') - julianday(window_start)) * 86400 - 3600
                        ) as session_seconds
                    FROM process_windows
                )
                SELECT
                    name,
                    CAST(COALESCE(SUM(session_seconds), 0) AS INTEGER) as total_seconds
                FROM time_sums
                GROUP BY name
                ORDER BY total_seconds DESC
                """
            ).fetchall()
            return [{'name': row['name'], 'total_seconds': row['total_seconds']} for row in results]


    def get_month_running_time(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            results = cursor.execute(
                """
                WITH process_windows AS (
                    -- First, identify distinct time windows for each process name
                    SELECT
                        p.name,
                        MIN(ps.start_time) as window_start,
                        CASE 
                            WHEN MAX(ps.end_time) IS NULL THEN 'now'
                            ELSE MAX(ps.end_time)
                        END as window_end
                    FROM processes p
                    JOIN process_sessions ps ON p.id = ps.process_session_id
                    WHERE strftime('%Y-%m', ps.start_time, 'localtime') = strftime('%Y-%m', 'now', 'localtime')
                    GROUP BY 
                        p.name,
                        -- Group by hourly windows to handle cases where the app was closed and reopened
                        strftime('%Y-%m-%d %H', ps.start_time)
                ),
                time_sums AS (
                    SELECT
                        name,
                        ROUND(
                            (julianday(window_end, 'localtime') - julianday(window_start)) * 86400 - 3600
                        ) as session_seconds
                    FROM process_windows
                )
                SELECT
                    name,
                    CAST(COALESCE(SUM(session_seconds), 0) AS INTEGER) as total_seconds
                FROM time_sums
                GROUP BY name
                ORDER BY total_seconds DESC
                """
            ).fetchall()
            return [{'name': row['name'], 'total_seconds': row['total_seconds']} for row in results]