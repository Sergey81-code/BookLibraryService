QUERY_TO_UNBLOCKING_PROCCESS_PG = """
    DO $$
    DECLARE
        rec RECORD;
    BEGIN
        FOR rec IN (
            SELECT 
                blocking_activity.pid AS blocking_pid
            FROM 
                pg_catalog.pg_locks blocked_locks
            JOIN 
                pg_catalog.pg_stat_activity blocked_activity
                ON blocked_activity.pid = blocked_locks.pid
            JOIN 
                pg_catalog.pg_locks blocking_locks
                ON blocking_locks.locktype = blocked_locks.locktype
                AND blocking_locks.database = blocked_locks.database
                AND blocking_locks.relation = blocked_locks.relation
                AND blocking_locks.pid != blocked_locks.pid
            JOIN 
                pg_catalog.pg_stat_activity blocking_activity
                ON blocking_activity.pid = blocking_locks.pid
            WHERE 
                blocked_locks.granted = false
        )
        LOOP
            EXECUTE format('SELECT pg_terminate_backend(%s);', rec.blocking_pid);
        END LOOP;
    END $$;
"""


QUERY_TO_DELETE_PROCESSES_PG = """    
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE 
        datname = current_database()
        AND pid <> pg_backend_pid()
        AND (state = 'idle in transaction' OR wait_event IS NOT NULL);
"""



CREATE_FAKE_TABLE_OF_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY
    )
"""