class Calendar:
    def __init__(self, connection):
        self.conn = connection

    def create_event(self, event_name, event_date, event_time, event_details):
        cur = self.conn.cursor()
        cur.execute('''
            INSERT INTO events (name, date, time, details)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        ''', (event_name, event_date, event_time, event_details))
        event_id = cur.fetchone()[0]
        self.conn.commit()
        return event_id

    def read_event(self, event_id):
        cur = self.conn.cursor()
        cur.execute('''
            SELECT * FROM events WHERE id=%s;
        ''', (event_id,))
        row = cur.fetchone()
        if row:
            return {'id': row[0], 'name': row[1], 'date': row[2], 'time': row[3], 'details': row[4]}
        return None

    def edit_event(self, event_id, updated_event):
        cur = self.conn.cursor()
        cur.execute('''
            UPDATE events SET name=%s, date=%s, time=%s, details=%s WHERE id=%s;
        ''', (updated_event["name"], updated_event["date"], updated_event["time"], updated_event["details"], event_id))
        rows_affected = cur.rowcount
        self.conn.commit()
        return bool(rows_affected)

    def delete_event(self, event_id):
        cur = self.conn.cursor()
        cur.execute('''
            DELETE FROM events WHERE id=%s;
        ''', (event_id,))
        rows_affected = cur.rowcount
        self.conn.commit()
        return bool(rows_affected)

    def list_events(self):
        cur = self.conn.cursor()
        cur.execute('''
            SELECT * FROM events ORDER BY date ASC, time ASC;
        ''')
        rows = cur.fetchall()
        return [{'id': r[0], 'name': r[1], 'date': r[2], 'time': r[3], 'details': r[4]} for r in rows]