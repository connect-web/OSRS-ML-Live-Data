from .base.server_connection import ServerConnection

class ResultsDatabase(ServerConnection):
    def usernamesToPlayerIds(self, player_usernames: list[str]) -> list[int]:
        query = '''
        SELECT id, name from players
        WHERE NAME = ANY(%s)
        '''
        rows = self.get(query, (player_usernames,))
        name_to_player_id = {row[1]: row[0] for row in rows}

        player_ids = []

        for username in player_usernames:
            player_id = name_to_player_id.get(username)
            if player_id is None:
                print(f'Username {username} not found in database.')
            else:
                player_ids.append(name_to_player_id[username])
        return player_ids

    def submit_results(self, player_ids: list[int], activity: str, ActivityType: str):
        """
        activity: name of skill / minigame
        ActivityType: (Skills) or (Minigames)
        """
        query = '''
        INSERT INTO ML.results(PlayerId, Activity, ActivityType, TIME)
        VALUES (%s, %s, %s, NOW())
        on conflict do nothing
        '''
        values = [(player_id, activity, ActivityType) for player_id in player_ids]
        self.post_many(query, values)


if __name__ == "__main__":
    db = ResultsDatabase()
    usernames = ['Zezima', 'Lynx Titan']
    playerIds = db.usernamesToPlayerIds(usernames)
    db.submit_results(playerIds, 'Clue Scrolls (all)', 'minigames')