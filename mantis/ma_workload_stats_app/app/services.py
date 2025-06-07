from datetime import datetime, timedelta
from collections import defaultdict

class WorkLoadService:
    def __init__(self, workload_data):
        self.workload_data = workload_data

    def get_bi_weekly_stats(self, personnel_id=None, team_id=None):
        return self._get_stats(timeframe='bi-weekly', personnel_id=personnel_id, team_id=team_id)

    def get_monthly_stats(self, personnel_id=None, team_id=None):
        return self._get_stats(timeframe='monthly', personnel_id=personnel_id, team_id=team_id)

    def _get_stats(self, timeframe, personnel_id, team_id):
        stats = defaultdict(lambda: defaultdict(int))
        end_date = datetime.now()
        
        if timeframe == 'bi-weekly':
            start_date = end_date - timedelta(weeks=2)
        elif timeframe == 'monthly':
            start_date = end_date - timedelta(days=30)
        else:
            raise ValueError("Invalid timeframe specified")

        for record in self.workload_data:
            record_date = datetime.strptime(record['date'], '%Y-%m-%d')
            if start_date <= record_date <= end_date:
                if personnel_id and record['personnel_id'] != personnel_id:
                    continue
                if team_id and record['team_id'] != team_id:
                    continue
                stats[record['personnel_id']]['workload'] += record['workload']
                stats[record['team_id']]['workload'] += record['workload']

        return dict(stats)