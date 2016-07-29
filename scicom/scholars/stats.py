"""Simple metric tracking for agreements issued."""

from datetime import datetime
from sqlalchemy import MetaData, Table, Column, types, select, func
from sqlalchemy.orm import mapper, create_session
from scicom.scholars.dbconn import DB_URI

class AgreementStatistic(object):
    """Tracking information for a single generated agreement."""
    
    def __init__(self, partner, journal, agreement):

        self.row_id = None
        self.issued = datetime.now()
        self.partner = partner
        self.journal = journal
        self.agreement = agreement

class StatsMapper(object):
    """An object mapper for agreement statistics."""

    def __init__(self):

        self.session = self._connect_session()
        
    def _connect_session(self):
        """Instantiate the database connection."""

        self.db_metadata = MetaData()
        self.db_metadata.bind = DB_URI

        # Agreement generation statistics
        self.agreements = Table('agreements', self.db_metadata,
                              Column('row_id', types.Integer,primary_key=True),
                              Column('issued', types.DateTime),
                              Column('partner', types.String(100)),
                              Column('journal', types.String(255)),
                              Column('agreement', types.String(255)),
                              )

        # make sure the table exists
        if not(self.agreements.exists()):
            self.agreements.create()

        self.mapper = mapper(AgreementStatistic, self.agreements)

        return create_session(bind=self.db_metadata.bind)

    def counts(self):
        """Return a sequence of tuples mapping, where each tuple consists of

        (journal, agreement_count)

        """

        s = select([self.agreements.c.journal,
                    func.count(self.agreements.c.row_id)]).\
                    group_by(self.agreements.c.journal)
        
        return self.session.connection().execute(s).fetchall()

    def total(self):
        """Return the total number of agreements issued."""

        s = select([func.count(self.agreements.c.row_id)])
        return self.session.connection().execute(s).fetchall()[0][0]
