from sqlalchemy import Column, Integer, Float

from .constants import Base

class C20XX_B(Base):
    """
    Model for IPEDS C20XX_B table
    """
    __tablename__ = 'c20xx_b'
    id = Column(Integer, primary_key = True)
    reporting_year = Column(Integer, nullable=False, comment="reporting year for record")
    unitid = Column(Integer, comment="Institution unit ID")
    cstotlt = Column(Integer, comment="Grand total")
    cstotlm = Column(Integer, comment="Grand total men")
    cstotlw = Column(Integer, comment="Grand total women")
    csaiant = Column(Integer, comment="American Indian or Alaska Native total")
    csaianm = Column(Integer, comment="American Indian or Alaska Native men")
    csaianw = Column(Integer, comment="American Indian or Alaska Native women")
    csasiat = Column(Integer, comment="Asian total")
    csasiam = Column(Integer, comment="Asian men")
    csasiaw = Column(Integer, comment="Asian women")
    csbkaat = Column(Integer, comment="Black or African American total")
    csbkaam = Column(Integer, comment="Black or African American men")
    csbkaaw = Column(Integer, comment="Black or African American women")
    cshispt = Column(Integer, comment="Hispanic or Latino total")
    cshispm = Column(Integer, comment="Hispanic or Latino men")
    cshispw = Column(Integer, comment="Hispanic or Latino women")
    csnhpit = Column(Integer, comment="Native Hawaiian or Other Pacific Islander total")
    csnhpim = Column(Integer, comment="Native Hawaiian or Other Pacific Islander men")
    csnhpiw = Column(Integer, comment="Native Hawaiian or Other Pacific Islander women")
    cswhitt = Column(Integer, comment="White total")
    cswhitm = Column(Integer, comment="White men")
    cswhitw = Column(Integer, comment="White women")
    cs2mort = Column(Integer, comment="Two or more races total")
    cs2morm = Column(Integer, comment="Two or more races men")
    cs2morw = Column(Integer, comment="Two or more races women")
    csunknt = Column(Integer, comment="Race/ethnicity unknown total")
    csunknm = Column(Integer, comment="Race/ethnicity unknown men")
    csunknw = Column(Integer, comment="Race/ethnicity unknown women")
    csnralt = Column(Integer, comment="Nonresident alien total")
    csnralm = Column(Integer, comment="Nonresident alien men")
    csnralw = Column(Integer, comment="Nonresident alien women")
