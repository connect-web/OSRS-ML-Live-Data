from .base.server_connection import ServerConnection
import json


class MetricsDatabase(ServerConnection):
    def submit_metric_dict(self, metrics: dict):
        rows = [
            (activity, json.dumps(metrics))
            for activity, metrics in metrics.items()
        ]
        query = '''
        INSERT INTO ML.metrics(activity, metrics, time)
        VALUES (%s, %s, NOW())
        ON CONFLICT (activity) DO UPDATE
        SET metrics = EXCLUDED.metrics,
            time = EXCLUDED.time
        '''
        self.post_many(query, rows)
