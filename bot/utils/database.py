import sqlite3

#from bot import se_db_path, channel_db_path

class seBoardDB:
    def set_database(tr_list: list):
        # Create table if it doesn't exist
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS seboard (id integer PRIMARY KEY, title text, author text)")

        latest_data_id = seBoardDB.get_latest_data_id()
        if latest_data_id is None:
            latest_data_id = [0]

        # add se board data
        for tr in tr_list:
            if tr[0] > latest_data_id[0]:
                c.execute(f"INSERT INTO seboard VALUES{tr}")
        conn.close()

    def get_database():
        # 모든 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM seboard ORDER BY id")
        except:
            return None
        temp = c.fetchall()
        conn.close()
        return temp
    
    def get_database_from_id(id):
        # id로 데이터베이스 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM seboard WHERE id=:Id", {"Id": id})
        except sqlite3.OperationalError:
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_latest_data_id():
        temp = seBoardDB.get_database()
        try:
            return temp[-1]
        except:
            return None

class channelDataDB:
    def channel_status_set(id: int, status: str):
        # Create table if it doesn't exist
        conn = sqlite3.connect(channel_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS broadcastChannel (id integer PRIMARY KEY, onoff text)")
        c.execute("SELECT * FROM userdata WHERE id=:id", {"id": id})
        a = c.fetchone()
        if a is None:
            # add channel set
            c.execute(f"INSERT INTO channel VALUES('{id}', '{status}')")
        else:
            # modify channel set
            c.execute("UPDATE channel SET onoff=:onoff WHERE id=:id", {"onoff": status, 'id': id})
        conn.close()
    
    def get_on_channel():
        # 모든 알람설정 되어있는 채널 가져오기
        conn = sqlite3.connect(se_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM channel ORDER BY id")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()

        on_channel = []
        for channel in temp:
            if temp[1] == "on":
                on_channel.append(channel[0])
        return on_channel

if __name__ == "__main__":
    se_db_path = "se_board.db"
    channel_db_path = "channel.db"
    post_list = [(82179, '각 학년 과대표 카카오톡 아이디 입니다. ', '12대 학생회장'), (82180, '[학생회] 2022년도 학과 학년 단톡방 개설 공지', '학생회')]
    seBoardDB.set_database(post_list)