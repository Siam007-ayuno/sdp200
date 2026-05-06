import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host='localhost', user='root', password='', database='safezone_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()

    def fetch_all_areas(self):
        if not self.is_connected():
            return []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM areas")
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetch_area_by_name(self, area_name):
        if not self.is_connected():
            return None
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM areas WHERE area_name = %s", (area_name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_reports_by_area(self, area_id):
        if not self.is_connected():
            return []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reports WHERE area_id = %s ORDER BY report_time DESC", (area_id,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_report(self, area_id, incident_type, severity, description, reporter_name, contact):
        if not self.is_connected():
            return False
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO reports (area_id, incident_type, severity, description, reporter_name, contact) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (area_id, incident_type, severity, description, reporter_name, contact)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            
            # Update area score after report
            self.update_area_safety_score(area_id)
            return True
        except Error as e:
            print(f"Error adding report: {e}")
            return False

    def update_area_safety_score(self, area_id):
        if not self.is_connected():
            return
        
        cursor = self.connection.cursor(dictionary=True)
        # MySQL syntax for interval
        cursor.execute("SELECT severity, incident_type FROM reports WHERE area_id = %s AND report_time >= NOW() - INTERVAL 30 DAY", (area_id,))
        recent_reports = cursor.fetchall()
        
        score = 100
        for rep in recent_reports:
            weight = 2
            if rep['incident_type'] in ['Violence', 'Harassment']:
                weight = 3
            elif rep['incident_type'] in ['Theft', 'Accident']:
                weight = 2
            else:
                weight = 1
            score -= (rep['severity'] * weight)
            
        if score < 0:
            score = 0
            
        status = 'Safe'
        if score < 40:
            status = 'Risky'
        elif score < 70:
            status = 'Moderate'
            
        update_query = "UPDATE areas SET current_score = %s, current_status = %s WHERE area_id = %s"
        cursor.execute(update_query, (score, status, area_id))
        self.connection.commit()
        cursor.close()

    def get_area_summary(self, area_id):
        if not self.is_connected():
            return None
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM areas WHERE area_id = %s", (area_id,))
        area = cursor.fetchone()
        
        cursor.execute("SELECT COUNT(*) as total_reports FROM reports WHERE area_id = %s AND report_time >= NOW() - INTERVAL 30 DAY", (area_id,))
        reports_count = cursor.fetchone()['total_reports']
        
        cursor.execute("SELECT incident_type, COUNT(*) as cnt FROM reports WHERE area_id = %s GROUP BY incident_type ORDER BY cnt DESC LIMIT 1", (area_id,))
        most_common = cursor.fetchone()
        common_type = most_common['incident_type'] if most_common else "N/A"
        
        cursor.close()
        return {
            "area_name": area['area_name'],
            "score": area['current_score'],
            "status": area['current_status'],
            "total_reports_30d": reports_count,
            "most_common_type": common_type
        }

    def verify_admin(self, username, password):
        if not self.is_connected():
            return False
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password_hash = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        return admin is not None
