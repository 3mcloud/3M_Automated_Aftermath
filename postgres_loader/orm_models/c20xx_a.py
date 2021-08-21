from sqlalchemy import Column, Integer, Float

from .constants import Base

class C20XX_A(Base):
    """
    Model for IPEDS C20XX_A table
    """
    __tablename__ = 'c20xx_a'
    id = Column(Integer, primary_key = True)
    reporting_year = Column(Integer, nullable=False, comment="reporting year for record")
    unitid = Column(Integer, comment="Institution unit ID")
    cipcode = Column(Float, comment="CIP code classification")
    awlevel = Column(Integer, comment="Award Level code")
    majornum = Column(Integer, comment="First or Second Major") 
    cnralm = Column(Integer, comment="Nonresident alien men")
    cnralw = Column(Integer, comment="Nonresident alien women")
    cunknm = Column(Integer, comment="Race/ethnicity unknown men")
    cunknw = Column(Integer, comment="Race/ethnicity unknown women")
    ctotalm = Column(Integer, comment="Grand total men")
    ctotalw = Column(Integer, comment="Grand total women")
    cnralt = Column(Integer, comment="Nonresident alien total")
    cunknt = Column(Integer, comment="Race/ethnicity unknown total")
    ctotalt = Column(Integer, comment="Grand total")
    chispm = Column(Integer, comment="Hispanic or Latino men")
    chispw = Column(Integer, comment="Hispanic or Latino women")
    caianm = Column(Integer, comment="American Indian or Alaska Native men")
    caianw = Column(Integer, comment="American Indian or Alaska Native women")
    casiam = Column(Integer, commment="Asian men")
    casiaw = Column(Integer, comment="Asian women")
    cbkaam = Column(Integer, comment="Black or African American men")
    cbkaaw = Column(Integer, comment="Black or African American women")
    cnhpim = Column(Integer, comment="Native Hawaiian or Other Pacific Islander men")
    cnhpiw = Column(Integer, comment="Native Hawaiian or Other Pacific Islander women")
    cwhitm = Column(Integer, comment="White men")
    cwhitw = Column(Integer, comment="White women")
    c2morm = Column(Integer, comment="Two or more races men")
    c2morw = Column(Integer, comment="Two or more races women")
    chispt = Column(Integer, comment="Hispanic or Latino total")
    caiant = Column(Integer, comment="American Indian or Alaska Native total")
    casiat = Column(Integer, comment="Asian total")
    cbkaat = Column(Integer, comment="Black or African American total")
    cnhpit = Column(Integer, comment="Native Hawaiian or Other Pacific Islander total")
    cwhitt = Column(Integer, comment="White total")
    c2mort = Column(Integer, comment="Two or more races total")

