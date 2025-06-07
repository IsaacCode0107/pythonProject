from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personnel(db.Model):
    __tablename__ = 'personnel'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    workloads = db.relationship('MA_WorkLoad', backref='personnel', lazy=True)

class Team(db.Model):
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    personnel = db.relationship('Personnel', backref='team', lazy=True)

class MA_WorkLoad(db.Model):
    __tablename__ = 'ma_workload'
    
    id = db.Column(db.Integer, primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    @staticmethod
    def get_bi_weekly_stats(personnel_id):
        # Logic to calculate bi-weekly statistics
        pass

    @staticmethod
    def get_monthly_stats(personnel_id):
        # Logic to calculate monthly statistics
        pass